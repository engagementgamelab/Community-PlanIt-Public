from django import forms

from web.responses.comment.models import *

#class CommentAttachmentResponseForm(forms.ModelForm):
#    message = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'comment_message'}))

#    class Meta:
#        model = CommentResponse
#        exclude = ('flagged', 'comments', 'posted_date')
