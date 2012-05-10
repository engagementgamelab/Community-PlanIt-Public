import datetime

from stream import utils as stream_utils
from stream.models import Action

from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
from django.shortcuts import redirect

from web.comments.forms import *
from web.comments.utils import create_video_attachment, create_image_attachment
from web.accounts.models import UserProfilePerInstance

import logging
log = logging.getLogger(__name__)

def _get_activity(pk, model_klass):
    trans_model = model_klass.objects.translations_model()
    try:
        return model_klass.objects.get(pk=pk)
    except trans_model.DoesNotExist:
        try:
            return model_klass.objects.language(settings.LANGUAGE_CODE).get(pk=pk)
        except trans_model.DoesNotExist:
            raise model_klass.DoesNotExist("activity translation could not be located. fallback does not exist.")

def comment_fun(answer, request, form=None, message=''):

    if hasattr(request, 'current_game'):
        current_instance = request.current_game
    else:
        raise Http404("could not locate a valid game")

    if form is not None:
        message = form.cleaned_data['message']
    comment = answer.comments.create(
                    content_object=answer,
                    message=message,
                    user=request.user,
                    instance=current_instance,
    )
    log.debug("challenge attachments %s" % request.FILES.keys())

    if request.POST.has_key('video-url'):
        create_video_attachment(comment, request.POST.get('video-url'), request.current_game, request.user)

    if request.FILES.has_key('picture'):
        create_image_attachment(comment, request.FILES.get('picture'), request.current_game, request.user)

def log_activity_and_redirect(request, activity, action_msg):

    if action_msg != "replayed":
        stream_utils.action.send(request.user,
                                verb='activity_%s' % action_msg,
                                action_object=activity,
                                target=request.current_game,
                                description="%s challenge" % action_msg
        )
    else:
        qs = Action.objects.filter(
                verb = 'activity_completed',
                actor_user=request.user,
        ).filter(
                Q(action_object_playeractivity=activity) | 
                Q(action_object_playermapactivity=activity) | 
                Q(action_object_playerempathyactivity=activity)
        )
        if qs.count() > 0:
            action = qs[0]
            action.datetime=datetime.datetime.now()
            action.save()

    # method of UserProfilePerInstance caches the
    # users total points per mission and percentage of missions total
    # points. invalidate here.
    # TODO only invalidate by one UserProfilePerInstance instance
    #cache.invalidate_group('my_progress_data')
    my_prof = request.user.get_profile()
    UserProfilePerInstance.objects.progress_data_for_mission.invalidate(request.current_game, activity.mission, my_prof)
    UserProfilePerInstance.objects.total_points_for_profile.invalidate(request.current_game, my_prof)
    return redirect(activity.get_overview_url())

