import datetime
from PIL import Image

from stream import utils as stream_utils
from stream.models import Action
from celery.execute import send_task

from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
#from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
#from django.contrib.contenttypes.models import ContentType

from comments.forms import *
from comments.models import Comment, Attachment
from web.attachments.tasks import run_attachment_checks
from web.accounts.models import UserProfilePerInstance
#from player_activities.models import PlayerActivity
#from reports.models import ActivityLogger
#from core.utils import instance_from_request

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

    if request.POST.has_key('video-url'):
        if request.POST.get('video-url'):
            attachment = Attachment.objects.create(
                    file=None,
                    url=request.POST.get('video-url'),
                    att_type=Attachment.ATTACHMENT_TYPE_VIDEO,
                    user=request.user,
                    instance=current_instance,
            )
            comment.attachment.add(attachment)
            log.debug("created attachment video url for comment %s. %s" % (comment.pk, attachment))
            #result = send_task("attachments.tasks.run_attachment_checks")
            #log.debug(result)

    if request.FILES.has_key('picture'):
        image_file = request.FILES.get('picture')
        picture = Image.open(image_file)
        if (image_file.name.rfind(".") -1):
            image_file.name = "%s.%s" % (image_file.name, picture.format.lower())

        attachment = Attachment.objects.create(
            file=image_file,
            att_type=Attachment.ATTACHMENT_TYPE_IMAGE,
            is_valid=True,
            user=request.user,
            instance=current_instance,
        )
        comment.attachment.add(attachment)
        log.debug("created attachment image for comment %s. %s" % (comment.pk, attachment))

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
    UserProfilePerInstance.objects.progress_data_for_mission(request.current_game, activity.mission, my_prof)
    UserProfilePerInstance.objects.total_points_for_profile.invalidate(request.current_game, my_prof)
    return HttpResponseRedirect(activity.get_overview_url())

# NOT USED
"""
def getComments(answers, ModelType, activity=None):
    comments = None
    if activity:
        act_type = ContentType.objects.get_for_model(PlayerActivity)
        comments = Comment.objects.filter(content_type=act_type, object_id=activity.pk)

    answer_type = ContentType.objects.get_for_model(ModelType)
    for answer in answers:
        if comments == None:
            comments = Comment.objects.filter(content_type=answer_type, object_id=answer.pk)
        else:
            comments = comments | Comment.objects.filter(content_type=answer_type, object_id=answer.pk)
    return comments
"""

