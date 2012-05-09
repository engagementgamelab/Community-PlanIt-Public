from sijax import Sijax
from PIL import Image
from stream import utils as stream_utils

from nani.utils import get_translation

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template import Context, RequestContext, loader, Template
from django.template.loader import render_to_string
from django.conf import settings

from web.accounts.models import UserProfile, UserProfilePerInstance
from web.reports.actions import PointsAssigner
from web.answers.models import Answer, AnswerMultiChoice
from web.challenges.models import Challenge
from web.values.models import Value
from .forms import *
from .models import Comment

#from web.attachments.models import Attachment

import logging
log = logging.getLogger(__name__)

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
        stream_utils.action.send(request.user, 'liked', target=c, description="liked a comment")
    return HttpResponse(str(c.likes.all().count()))

def notify_author(request, comment_parent, comment):
    message = None
    recipient = None

    if isinstance(comment_parent, UserProfilePerInstance):
        if request.user != comment_parent.user_profile.user:
            recipient = comment_parent.user_profile.user
            message = '%s commented on your profile.' % request.user.get_profile().screen_name

    elif isinstance(comment_parent, Comment):
        if request.user != comment_parent.user:
            topic = comment_parent.topic
            #if isinstance(topic, Challenge):
            #    message = "%s replied to a comment on %s" % (
            #        request.user.get_profile().screen_name,
            #        topic
            #    )
            #    recipient = topic.user
            #elif isinstance(topic, UserProfile):
            #    message = "%s replied to a comment on your profile" % (
            #        request.user.get_profile().screen_name
            #    )
            #    recipient = topic.user
            #else:
            #    message = "%s replied to your comment on %s" % (
            #        request.user.get_profile().screen_name,
            #        topic
            #    )
            #    recipient = parent_comment.user
            if isinstance(topic, Answer) or isinstance(topic, AnswerMultiChoice):
                message = "%s replied to your answer %s" %(
                    request.user.get_profile().screen_name,
                    topic
                )
                try:
                    recipient = topic.answerUser
                except AttributeError:
                    recipient = topic.user

    if recipient is not None and message is not None:
        recipient.notifications.create(content_object=comment, message=message)


@login_required
def ajax_create(request, comment_form=CommentForm):

    request_uri = reverse('comments:ajax-create')

    def create(obj_response, form_data):
        log.debug("creating comment: %s" % form_data)
        form = comment_form(data=form_data)
        if form.is_valid():
            cd = form.cleaned_data
            log.debug("processed comment_form. cleaned_data: %s" % cd)
            # convert this to work for other types of parent objects
            parent_type = cd.get('parent_type')
            if parent_type == 'user_profile':
                comment_parent  = get_object_or_404(UserProfilePerInstance, id=cd.get('parent_id'))
                stream_description = "commented on a user profile"
            elif parent_type == 'map_the_future':
                comment_parent  = get_object_or_404(Value, id=cd.get('parent_id'))
                stream_description = "commented on a priority"
            elif parent_type == 'comment':
                comment_parent  = get_object_or_404(Comment, id=cd.get('parent_id'))
                stream_description = "commented on a comment"
            instance = comment_parent.instance

            c = comment_parent.comments.create(
                content_object=comment_parent,
                message=cd.get(u'message'),
                user=request.user,
                instance=instance,
            )
            log.debug("comment created. %s" % vars(c))
            stream_verb = 'commented'
            stream_utils.action.send(
                            request.user,
                            stream_verb,
                            target=comment_parent,
                            action_object=c,
                            description=stream_description
            )
            notify_author(request, comment_parent, c)

            #from celery.execute import send_task
            #result = send_task("badges.tasks.gen_badges", [request.user.pk, stream_verb, action_object_])
            #print result.get()
            #from badges.tasks import gen_badges
            #user_id=request.user.pk
            #task_kwargs = dict(
            #        stream_verb=stream_verb,
            #)
            # gen_badges.apply_async(args=[user_id,], kwargs=task_kwargs)

            if parent_type == 'user_profile':
                obj_response.redirect(
                            reverse('accounts:player_profile', 
                                    args=(comment_parent.user_profile.user.pk,)
                            )
                )

            elif parent_type == 'map_the_future':
                obj_response.redirect(
                            reverse('values:detail', 
                                    args=(comment_parent.pk,)
                            )
                )
            elif parent_type == 'comment':
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


@login_required
def reply(request, id):
    parent_comment = get_object_or_404(Comment, id=id)
    instance = parent_comment.instance
  
    c = parent_comment.comments.create(
        content_object=parent_comment,
        message=request.POST.get(u'message'), 
        user=request.user,
        instance=instance,
    )
    PointsAssigner().assign(request.user, 'comment_created')

    topic = parent_comment.topic

    recipient = None
    if request.user != parent_comment.user:
        if isinstance(topic, Challenge):
            message = "%s replied to a comment on %s" % (
                request.user.get_profile().screen_name,
                topic
            )
            recipient = topic.user
        elif isinstance(topic, UserProfile):
            message = "%s replied to a comment on your profile" % (
                request.user.get_profile().screen_name
            )
            recipient = topic.user
        else:
            message = "%s replied to your comment on %s" % (
                request.user.get_profile().screen_name,
                topic
            )
            recipient = parent_comment.user

    if recipient:
        recipient.notifications.create(content_object=c, message=message)
    return HttpResponseRedirect(c.get_absolute_url())

@login_required
def edit(request, id, lang_code=None):    
    comment = get_object_or_404(Comment, id=id)    
    
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        s = ""
        for x in request.POST.keys():
            s = "%s%s: %s<br>" % (s, x, request.POST[x])
        s = "%s<br> FILES<br>" % s
        for x in request.FILES.keys():
            s = "%s%s: %s" % (s, x, request.FILES[x])
        #return HttpResponse(s)
        
        
        if comment_form.is_valid(): 
            comment.message = comment_form.cleaned_data['message']
            comment.save()
            
            #TODO: This is where the attachments are cleared out for the comment. 
            # This needs to change when the ability to upload a different picture or 
            # remove the existing picture functionality changes. Also note that each comment
            # can only have one attachment, this needs to be enforced. 
            comment.attachment.clear()

            if request.POST.has_key(u'video-url'):
                if request.POST.get(u'video-url'):
                    comment.attachment.create(
                            file=None,
                            url=request.POST.get(u'video-url'),
                            type=u'video',
                            user=request.user,
                            instance=request.user.get_profile().instance)
            
            if request.FILES.has_key(u'picture'):
                file = request.FILES.get(u'picture')
                picture = Image.open(file)
                if (file.name.rfind(".") -1):
                    file.name = "%s.%s" % (file.name, picture.format.lower())
                comment.attachment.create(
                    file=request.FILES.get(u'picture'),
                    user=request.user,
                    instance=request.user.get_profile().instance)
            return HttpResponseRedirect(comment.get_absolute_url())

    comment_form = CommentForm(initial={'message': comment.message})
   
    tmpl = loader.get_template(u'comments/edit.html')
    
    if comment.user != request.user:
        return HttpResponse(tmpl.render(RequestContext(request, {"not_permitted": True }, 
            )))
    else:
        return HttpResponse(tmpl.render(RequestContext(request, {"comment": comment,
                                                                 "comment_form": comment_form }, 
                                                                 )))

#@login_required
#def remove_attachment(request, id, comment_id):
#    attachment = get_object_or_404(Attachment, id=id)
#    comment = get_object_or_404(Comment, id=comment_id) 
#    attachment.delete()
#    return HttpResponseRedirect(reverse("comments:edit", args=[comment.pk,]))
    
