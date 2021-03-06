from django import forms

class CommentForm(forms.Form):
    # sometimes we don't want to show the entire discussion
    # before the user has contributed
    just_one_form = False
    allow_replies = True
    parent_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    parent_type = forms.CharField(widget=forms.HiddenInput(), required=False)
    message = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(
            attrs = {
                'rows': 6,
                'cols': 80,
            }
        ),
        label='Comment'
    )

    def __init__(self, *args, **kwargs):
        if 'just_one_form' in kwargs:
            self.just_one_form = True
            del kwargs['just_one_form']
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        message = self.cleaned_data.get('message')

        if message:
            if message.strip() == '':
                raise forms.ValidationError("Please enter a valid message")

        return self.cleaned_data
