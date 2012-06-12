from web.flags.models import PlayerFlag
from web.comments.models import Comment
#from web.challenges.models import Challenge

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def add(request, app, id):
    id = int(id)
    if app == 'account':
        u = User.objects.get(id=id)
        label = u.username

        p = u.get_profile()
        p.flagged += 1
        p.save()

    elif app == 'comment':
        c = Comment.objects.get(id=id)
        label = c.message

        c.flagged += 1
        c.save()

    #elif app == 'challenge':
    #    c = Challenge.objects.get(id=id)
    #    label = c.name

    #    c.flagged += 1
    #    c.save()

    if len(PlayerFlag.objects.filter(app=app, id=id, user=request.user)) == 0:
        pf = PlayerFlag(
            app = app,
            app_id = id,
            label = label,
            user = request.user,
        )

        pf.save()
        messages.success(request, 'Flagged ' + app)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
