from django import forms

class CommentForm(forms.Form):
    # sometimes we don't want to show the entire discussion
    # before the user has contributed
    just_one_form = False

    message = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(
            attrs = {
                'rows': 6,
                'cols': 80,
            }
        ),
        label='Comment',
        help_text=(
            '<div class="fine counter">(<span class="count">1000</span>'
            ' characters left)</div>'
        )
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
