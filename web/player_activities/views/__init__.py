from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from comments.forms import *
from comments.models import Comment

def _get_activity(pk, model_klass):
    trans_model = model_klass.objects.translations_model()
    try:
        return model_klass.objects.get(pk=pk)
    except trans_model.DoesNotExist:
        return model_klass.objects.language(settings.LANGUAGE_CODE).get(pk=pk)

def _get_translatable_field(instance, field_name):
    val = None
    trans_model = instance.__class__.objects.translations_model()
    try:
        return getattr(instance, field_name)
    except trans_model.DoesNotExist:
        for trans in instance.translations.all():
            if trans.language_code == settings.LANGUAGE_CODE:
                return trans.value
    return val or "n/a"


def comment_fun(answer, form, request):
    comment = answer.comments.create(
        content_object=answer,
        message=form.cleaned_data['message'], 
        user=request.user,
        instance=request.user.get_profile().instance,
    )
    
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

def process_comment(request, activity):
    """
    Lovely side-effect programming, this. That monstrous overview method needs
    refactoring in the worst way.
    """

    if request.method == 'POST':
        print "POSTED COMMENT"
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            print "VALID FORM:", comment_form
            comment = Comment.objects.create(
                content_object=activity,
                message=comment_form.cleaned_data['message'], 
                user=request.user,
                instance=activity.mission.instance,
            )
            print "COMMENT CREATED:", comment
            if request.POST.has_key('yt-url'):
                if request.POST.get('yt-url'):
                    comment.attachment.create(
                            file=None,
                            url=request.POST.get('yt-url'),
                            type='video',
                            user=request.user,
                            instance=activity.mission.instance)
            
            if request.FILES.has_key('picture'):
                file = request.FILES.get('picture')
                picture = Image.open(file)
                if (file.name.rfind(".") -1):
                    file.name = "%s.%s" % (file.name, picture.format.lower())
                comment.attachment.create(
                    file=request.FILES.get('picture'),
                    user=request.user,
                    instance=activity.mission.instance)
    else:
        comment_form = CommentForm()

    return comment_form

def getComments(answers, ModelType):
    comments = None
    answer_type = ContentType.objects.get_for_model(ModelType)
    for answer in answers:
        if comments == None:
            comments = Comment.objects.filter(content_type=answer_type, object_id=answer.pk)
        else:
            comments = comments | Comment.objects.filter(content_type=answer_type, object_id=answer.pk)
    return comments
