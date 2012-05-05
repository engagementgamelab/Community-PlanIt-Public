import datetime
from PIL import Image

from stream import utils as stream_utils
from stream.models import Action

from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType

from PIL import Image

from comments.forms import *
from comments.models import Comment, Attachment
from player_activities.models import PlayerActivity
from reports.models import ActivityLogger
#from core.utils import instance_from_request

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
            comment.attachment.create(
                    file=None,
                    url=request.POST.get('video-url'),
                    att_type=Attachment.ATTACHMENT_TYPE_VIDEO,
                    user=request.user,
                    instance=current_instance)
    
    if request.FILES.has_key('picture'):
        file = request.FILES.get('picture')
        picture = Image.open(file)
        if (file.name.rfind(".") -1):
            file.name = "%s.%s" % (file.name, picture.format.lower())
        comment.attachment.create(
            file=request.FILES.get('picture'),
            att_type=Attachment.ATTACHMENT_TYPE_IMAGE,
            is_valid=True,
            user=request.user,
            instance=current_instance)

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
    cache.invalidate_group('my_progress_data')
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

