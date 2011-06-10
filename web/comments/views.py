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
def like(request, id):
    c = Comment.objects.get(id=id)
    if request.user != c.user:
        c.likes.add(request.user)
    referrer = request.META['HTTP_REFERER'].split('#', 1)[0]
    referrer += '#comment-%s' % c.pk
    return HttpResponseRedirect(referrer)

@login_required
def reply(request, id):
    p = Comment.objects.get(id=id)
    instance = request.user.get_profile().instance
  
    c = p.comments.create(
        message=request.POST.get('message'), 
        user=request.user,
        instance=instance,
    )

    referrer = request.META['HTTP_REFERER'].split('#', 1)[0]
    referrer += '#comment-%s' % c.pk
    return HttpResponseRedirect(referrer)
