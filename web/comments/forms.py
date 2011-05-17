from django import forms

class CommentForm(forms.Form):
    message = forms.CharField(max_length=140, widget=forms.Textarea, label='Comment', help_text='<br><span class="fine">(<span class="count">140</span> characters left)</span>')

    def clean(self):
        message = self.cleaned_data.get('message')

        if message:
            if message.strip() == '':
                raise forms.ValidationError("Please enter a valid message")

        return self.cleaned_data
