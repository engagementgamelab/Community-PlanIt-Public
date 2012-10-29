from sijax import Sijax
from PIL import Image
from stream import utils as stream_utils

# from nani.utils import get_translation

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template import Context, RequestContext, loader, Template
from django.template.loader import render_to_string
from django.conf import settings
from django.views.generic.base import TemplateView
from web.accounts.mixins import MissionContextMixin

from web.accounts.models import UserProfile, UserProfilePerInstance
# from web.reports.actions import PointsAssigner
# from web.challenges.models import Answer, AnswerMultiChoice
from web.values.models import Value
from .forms import *
from .models import Comment

import logging
log = logging.getLogger(__name__)

class BuzzView(MissionContextMixin, TemplateView):
    template_name = 'public_square/buzz.html'

buzz_view = BuzzView.as_view()

class SoapboxView(MissionContextMixin, TemplateView):
    template_name = 'public_square/soapbox.html'

soapbox_view = SoapboxView.as_view()

@login_required
def flag(request, id):
    c = Comment.objects.get(id=id)
    c.flagged = c.flagged+1
    c.save()

    return HttpResponseRedirect(c.get_absolute_url())

# deprecated. ajax only now
#@login_required
#def like(request, id):
#    c = Comment.objects.get(id=id)
#    if request.user != c.user:
#        c.likes.add(request.user)
#        message = u"%s liked your comment on %s" % (
#            request.user.get_profile().screen_name,
#            c.content_object
#        )
#        c.user.notifications.create(content_object=c, message=message)
#    return HttpResponseRedirect(c.get_absolute_url())

@login_required
def ajax_like(request, id):
    if not request.is_ajax():
        return HttpResponse("")

    try:
        c = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return HttpResponse("")

    if request.user != c.user and not request.user in c.likes.all():
        c.likes.add(request.user)
        message = u"%s liked your comment on %s" % (
            request.user.get_profile().screen_name, c.content_object
        )
        c.user.notifications.create(content_object=c, message=message)
        stream_utils.action.send(request.user, 'liked', target=c, description="liked the comment")
    return HttpResponse(str(c.likes.all().count()))

def notify_author(request, comment_parent, comment):
    message = None
    recipient = None

    if isinstance(comment_parent, Comment) and \
            request.user != comment_parent.user:

        topic = comment_parent.topic

        challenge = None
        if isinstance(topic, AnswerMultiChoice):
            challenge = topic.option.activity
        elif hasattr(topic, 'activity'):
            challenge = topic.activity

        if isinstance(topic, Answer) or isinstance(topic, AnswerMultiChoice):
            message = "%s replied to your answer %s." %(
                request.user.get_profile().screen_name,
                topic
            )
            try:
                recipient = topic.answerUser
            except AttributeError:
                recipient = topic.user

        if recipient is not None and message is not None:
            recipient.notifications.create(content_object=comment, message=message)

        for comment in comment_parent.comments.all():
            if comment.user == request.user:
                continue
            message = "%s also replied to the response to %s." %(
                    request.user.get_profile().screen_name,
                    challenge,
            )
            comment.user.notifications.create(
                    content_object=comment, 
                    message=message
            )

@login_required
def ajax_create(request, comment_form=CommentForm):

    request_uri = reverse('comments:ajax-create')

    def create(obj_response, form_data):
        log.debug("creating comment: %s" % form_data)
        form = comment_form(data=form_data)
        if form.is_valid():
            cd = form.cleaned_data
            comment_parent  = get_object_or_404(Comment, id=cd.get('parent_id'))
            comment = comment_parent.comments.create(
                content_object=comment_parent,
                message=cd.get(u'message'),
                user=request.user,
                instance=comment_parent.instance,
            )
            stream_utils.action.send(
                            actor=request.user,
                            verb='commented',
                            target=comment_parent,
                            action_object=comment,
                            description="commented on a comment"
            )
            notify_author(request, comment_parent, comment)

            #from celery.execute import send_task
            #result = send_task("badges.tasks.gen_badges", [request.user.pk, stream_verb, action_object_])
            #print result.get()
            #from badges.tasks import gen_badges
            #user_id=request.user.pk
            #task_kwargs = dict(
            #        stream_verb=stream_verb,
            #)
            # gen_badges.apply_async(args=[user_id,], kwargs=task_kwargs)

            context = dict(
                comment = comment_parent,
                STATIC_URL = settings.STATIC_URL,
                MEDIA_URL = settings.MEDIA_URL,
                request = request,
            )
            rendered_comments = render_to_string('comments/nested_replies.html', context)
            obj_response.html('#replies-'+str(comment_parent.pk), rendered_comments)
            obj_response.call('init_masonry')
        else:
            log.debug("form errors: %s" % form.errors)

    instance = Sijax()
    instance.set_data(request.POST)
    instance.set_request_uri(request_uri)
    instance.register_callback('create_comment', create)
    if instance.is_sijax_request:
        return HttpResponse(instance.process_request())
