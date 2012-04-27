from sijax import Sijax
from PIL import Image
from stream import utils as stream_utils

from nani.utils import get_translation

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template import Context, RequestContext, loader, Template
from django.conf import settings


from accounts.models import UserProfile
from reports.actions import PointsAssigner
from answers.models import Answer
from challenges.models import Challenge
from .forms import *
from .models import Comment

from attachments.models import Attachment

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


@login_required
def ajax_create(request, comment_form=CommentForm):
    request_uri = reverse('comments:ajax-create')
    def create(obj_response, form_data):
        log.debug("creating comment: %s" % form_data)
        form = comment_form(data=form_data)
        if form.is_valid():
            cd = form.cleaned_data
            parent_comment = get_object_or_404(Comment, id=cd.get('parent_comment_id'))
            instance = parent_comment.instance

            c = parent_comment.comments.create(
                content_object=parent_comment,
                message=cd.get(u'message'),
                user=request.user,
                instance=instance,
            )
            log.debug("comment created. %s" % vars(c))
            stream_verb = 'commented'
            stream_utils.action.send(request.user, stream_verb, target=parent_comment, action_object=c, description="commented on a comment")

            #from celery.execute import send_task
            #result = send_task("badges.tasks.gen_badges", [request.user.pk, stream_verb, action_object_])
            #print result.get()
            from badges.tasks import gen_badges
            user_id=request.user.pk
            task_kwargs = dict(
                    stream_verb=stream_verb,
            )
            gen_badges.apply_async(args=[user_id,], kwargs=task_kwargs)


            context = dict(
                comment = parent_comment,
                STATIC_URL = settings.STATIC_URL,
                request = request,
            )
            players_tmpl = """\
                <div class="nested replies" id="replies-{{comment.pk}}">
                    {% for comment in comment.comments.all %}
                        {% with filename="comments/comment.html" extra_message=None %}
                            {% include filename %}
                        {% endwith %}
                    {% endfor %}
                    <div style="clear:both"></div>
                </div> """
            t = Template(players_tmpl)
            rendered_comments = t.render(Context(context))
            obj_response.html('#id_replies-'+str(parent_comment.pk), rendered_comments)
        else:
            print "form errors; ", form.errors

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

@login_required
def remove_attachment(request, id, comment_id):
    attachment = get_object_or_404(Attachment, id=id)
    comment = get_object_or_404(Comment, id=comment_id) 
    attachment.delete()
    return HttpResponseRedirect(reverse("comments:edit", args=[comment.pk,]))
    
