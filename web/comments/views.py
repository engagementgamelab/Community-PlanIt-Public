from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from web.accounts.models import UserProfile
from web.challenges.models import Challenge
from web.comments.models import Comment

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
    p = Comment.objects.get(id=id)
    instance = request.user.get_profile().instance
  
    c = p.comments.create(
        content_object=p,
        message=request.POST.get('message'), 
        user=request.user,
        instance=instance,
    )

    topic = p.topic

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

    recipient.notifications.create(content_object=c, message=message)

    return HttpResponseRedirect(c.get_absolute_url())
