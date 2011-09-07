from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import Context, RequestContext, loader
from django.conf import settings

from nani.utils import get_translation

from web.accounts.models import UserProfile
from web.answers.models import Answer
from web.challenges.models import Challenge
from web.comments.forms import *
from web.comments.models import Comment
#from web.processors import instance_processor as ip

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
    p = Comment.objects.untranslated().get(id=id)
    instance = request.user.get_profile().instance
  
    c = p.comments.create(
        content_object=p,
        message=request.POST.get('message'), 
        user=request.user,
        instance=instance,
    )

    topic = p.topic

    recipient = None
    if request.user != p.user:
        message = "%s replied to your comment on %s" % (
            request.user.get_profile().screen_name,
            topic
        )
        recipient = p.user
    elif isinstance(topic, Challenge):
        message = "%s replied to a comment on %s" % (
            request.user.get_profile().screen_name,
            topic
        )
        recipient = topic.player
    elif isinstance(topic, UserProfile):
        message = "%s replied to a comment on your profile" % (
            request.user.get_profile().screen_name
        )
        recipient = topic.user

    if recipient:
        recipient.notifications.create(content_object=c, message=message)

    return HttpResponseRedirect(c.get_absolute_url())

@login_required
def edit(request, id, lang_code=None):    
    comment = Comment.objects.untranslated().get(id=id)    
    #instance = request.user.get_profile().instance
    trans = None
    for language_code, _lang_name in settings.LANGUAGES:
        try:
            trans = get_translation(comment, language_code)
            break
        except:
            pass
    if trans is not None:
        comment = Comment.objects.language(trans.language_code).get(id=id)    
    
    comment_form = CommentForm(data=request.POST or None)
    comment_form.allow_replies = False
    
    if request.method == "POST":
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
            #TODO: what if answer does not exist?
            try:            
                activity_id = Answer.objects.get(id=comment.object_id).activity.id
                return HttpResponseRedirect(reverse("activities:overview", args=[activity_id]))
            except Answer.DoesNotExist:
                return HttpResponseRedirect(reverse('accounts_profile', args=[request.user.pk]))
                
       
   
    tmpl = loader.get_template('comments/edit.html')
    
    if comment.user != request.user:
        return HttpResponse(tmpl.render(RequestContext(request, {"not_permitted": True }, 
            #[ip]
            )))
    else:
        return HttpResponse(tmpl.render(RequestContext(request, {"comment": comment,
                                                                 "comment_form": comment_form }, 
                                                                 #[ip]
                                                                 )))
                                                                 

    
