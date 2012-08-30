from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape

from .models import *
from web.missions.models import Mission


import logging
log = logging.getLogger(__name__)


class SingleResponseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        challenge = kwargs.get('initial')['challenge']
        super(SingleResponseForm, self).__init__(*args, **kwargs)

        self.fields['selected'] = forms.ModelChoiceField(
                    widget=forms.widgets.RadioSelect,
                    required=True,
                    empty_label=None,
                    queryset=AnswerChoice.objects.\
                            filter(challenge=challenge).distinct()
        )

    class Meta:
        model = AnswerWithOneChoice
        exclude = ('user', 'challenge')


class MultiResponseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        challenge = kwargs.get('initial')['challenge']
        super(MultiResponseForm, self).__init__(*args, **kwargs)

        self.fields['selected'] = forms.ModelMultipleChoiceField(
                    widget=forms.widgets.CheckboxSelectMultiple,
                    required=True,
                    queryset=AnswerChoice.objects.\
                            filter(challenge=challenge).distinct()
        )

    class Meta:
        model = AnswerWithMultipleChoices
        exclude = ('user', 'challenge')


class BarrierRadioInput(forms.widgets.RadioInput):

    def __init__(self, *args, **kwargs):
        choice_statuses = kwargs.pop('choice_statuses')
        super(BarrierRadioInput, self).__init__(*args, **kwargs)

    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if 'id' in self.attrs:
            label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = conditional_escape(force_unicode(self.choice_label))

        dark_background_css = 'class="radio-item-disabled"'
        #background: none repeat scroll 0 0 #DDDDDD;"'

        return mark_safe(u'<label%s %s>%s %s</label>' % (label_for, dark_background_css, self.tag(), choice_label))

class BarrierFieldRenderer(forms.widgets.RadioFieldRenderer):

    """ Modifies some of the Radio buttons to be disabled in HTML,
    based on an externally-appended choice_statuses list. """

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield BarrierRadioInput(self.name, self.value, self.attrs.copy(), choice, i, choice_statuses=self.choice_statuses)

    def render(self):
        if not hasattr(self, "choice_statuses"):
            return self.original_render()
        return self.my_render()

    def original_render(self):
        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>'
            % force_unicode(w) for w in self]))

    def my_render(self):
        midList = []
        for x, wid in enumerate(self):
            if self.choice_statuses[x]:
                wid.attrs['disabled'] = True
            midList.append(u'<li>%s</li>' % force_unicode(wid))
        finalList = mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>'
            % w for w in midList])
        )
        return finalList


class BarrierFiftyFiftyForm(forms.Form):

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance')
        initial_data = kwargs.pop('initial')
        challenge = initial_data.get('challenge')
        super(BarrierFiftyFiftyForm, self).__init__(*args, **kwargs)

        self.fields['selected'] = forms.ChoiceField(required=True)
        self.fields['selected'].widget = forms.widgets.RadioSelect(
                renderer=BarrierFieldRenderer
        )
        self.fields['selected'].choices=AnswerChoice.objects.\
                                            by_challenge(challenge).\
                                            values_list('pk', 'value')
        self.fields['selected'].widget.renderer.choice_statuses = challenge.random_answer_choices

