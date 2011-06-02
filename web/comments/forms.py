from django import forms

class CommentForm(forms.Form):
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

    def clean(self):
        message = self.cleaned_data.get('message')

        if message:
            if message.strip() == '':
                raise forms.ValidationError("Please enter a valid message")

        return self.cleaned_data
