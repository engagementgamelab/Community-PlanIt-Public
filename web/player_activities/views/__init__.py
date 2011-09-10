from django.conf import settings
from django.contrib.contenttypes.models import ContentType

def _get_activity(pk, model_klass):
    trans_model = model_klass.objects.translations_model()
    try:
        return model_klass.objects.get(pk=pk)
    except trans_model.DoesNotExist:
        return model_klass.objects.language(settings.LANGUAGE_CODE).get(pk=pk)

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

def getComments(answers, ModelType):
    comments = None
    answer_type = ContentType.objects.get_for_model(ModelType)
    for answer in answers:
        if comments == None:
            comments = Comment.objects.language(get_language()).filter(content_type=answer_type, object_id=answer.pk)
        else:
            comments = comments | Comment.objects.language(get_language()).filter(content_type=answer_type, object_id=answer.pk)
    return comments
