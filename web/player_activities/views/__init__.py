from PIL import Image

from stream import utils as stream_utils

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType

from PIL import Image

from comments.forms import *
from comments.models import Comment
from player_activities.models import PlayerActivity
from reports.models import ActivityLogger
from core.utils import instance_from_request

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

    current_instance = instance_from_request(request)

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
                    type='video',
                    user=request.user,
                    instance=current_instance)
    
    if request.FILES.has_key('picture'):
        file = request.FILES.get('picture')
        picture = Image.open(file)
        if (file.name.rfind(".") -1):
            file.name = "%s.%s" % (file.name, picture.format.lower())
        comment.attachment.create(
            file=request.FILES.get('picture'),
            user=request.user,
            instance=current_instance)

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

def log_activity_and_redirect(request, activity, message):
    #ActivityLogger().log(request.user, request, "the activity: " + activity.name[:30] + "...", message, activity.get_activity_url(), "activity")
    stream_utils.action.send(request.user, 'activity_%s' % message, action_object=activity,
                            description="%s activity" % message
    )

    return HttpResponseRedirect(activity.get_overview_url())   


