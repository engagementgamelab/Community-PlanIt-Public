from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template import Context, RequestContext, loader
from django.conf import settings

from nani.utils import get_translation

from web.accounts.models import UserProfile
from web.reports.actions import PointsAssigner
from web.answers.models import Answer
from web.challenges.models import Challenge
from web.comments.forms import *
from web.comments.models import Comment

from PIL import Image


@login_required
def flag(request, id):
    c = Comment.objects.get(id=id)
    c.flagged = c.flagged+1
    c.save()

    return HttpResponseRedirect(c.get_absolute_url())

@login_required
def like(request, id):
    c = Comment.objects.get(id=id)
    if request.user != c.user:
        c.likes.add(request.user)
        message = "%s liked your comment on %s" % (
            request.user.get_profile().screen_name,
            c.content_object
        )
        c.user.notifications.create(content_object=c, message=message)
    return HttpResponseRedirect(c.get_absolute_url())

@login_required
def reply(request, id):
    parent_comment = get_object_or_404(Comment, id=id)
    instance = parent_comment.instance
  
    c = parent_comment.comments.create(
        content_object=parent_comment,
        message=request.POST.get('message'), 
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

            if request.POST.has_key('yt-url'):
                if request.POST.get('yt-url'):
                    comment.attachment.create(
                            file=None,
                            url=request.POST.get('yt-url'),
                            type='video',
                            user=request.user,
                            instance=request.user.get_profile().instance)
            
            if request.FILES.has_key('picture'):
                file = request.FILES.get('picture')
                picture = Image.open(file)
                if (file.name.rfind(".") -1):
                    file.name = "%s.%s" % (file.name, picture.format.lower())
                comment.attachment.create(
                    file=request.FILES.get('picture'),
                    user=request.user,
                    instance=request.user.get_profile().instance)
            return HttpResponseRedirect(comment.get_absolute_url())

    comment_form = CommentForm(initial={'message': comment.message})
   
    tmpl = loader.get_template('comments/edit.html')
    
    if comment.user != request.user:
        return HttpResponse(tmpl.render(RequestContext(request, {"not_permitted": True }, 
            )))
    else:
        return HttpResponse(tmpl.render(RequestContext(request, {"comment": comment,
                                                                 "comment_form": comment_form }, 
                                                                 )))
                                                                 

    
