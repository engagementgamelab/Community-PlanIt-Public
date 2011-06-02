from django import forms

from web.responses.comment.models import *

class CommentResponseForm(forms.ModelForm):
    message = forms.CharField(max_length=1000,widget=forms.Textarea)

    class Meta:
        model = CommentResponse
        exclude = ('flagged','comments','attachment')

class CommentAttachmentResponseForm(forms.ModelForm):
    message = forms.CharField(max_length=1000,widget=forms.Textarea)

    class Meta:
        model = CommentResponse
        exclude = ('flagged','comments')
