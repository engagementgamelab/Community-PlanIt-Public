from web.comments.models import Comment
from web.comments.forms import *

def post(request, form):
    instance = request.user.get_profile().instance
    comment = Comment(
        message = form.cleaned_data['message'],
        user = request.user,
        instance = instance,
    )
    comment.save()
    return comment
