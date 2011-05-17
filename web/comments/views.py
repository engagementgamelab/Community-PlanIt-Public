from django.http import HttpResponse, HttpResponseRedirect

from web.comments.models import Comment
from django.contrib.auth.decorators import login_required

@login_required
def flag(request, id):
    c = Comment.objects.get(id=id)
    c.flagged = c.flagged+1
    c.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def reply(request, id):
    p = Comment.objects.get(id=id)
    instance = request.user.get_profile().instance
  
    c = Comment(
        message=request.POST.get('message'), 
        user=request.user,
        instance=instance,
    )

    c.save()

    p.comments.add(c)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
