from django import forms
from django.contrib.comments.forms import CommentForm
from .models import PlayerComment

class PlayerCommentForm(CommentForm):
    hidden = forms.BooleanField(required=False)

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return PlayerComment

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in new fields
        data = super(PlayerComment, self).get_comment_create_data()
        data['hidden'] = self.cleaned_data['hidden']
        return data
