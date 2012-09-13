from sijax import Sijax

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage

from django.db.models import Q
from django.shortcuts import redirect
from django.db import transaction
from django.template import Context, RequestContext, loader
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, ugettext, ugettext_lazy as _

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.formtools.wizard.views import SessionWizardView

from .models import *
from web.instances.models import Instance, Affiliation

from web.core.utils import get_translation_with_fallback

import logging
log = logging.getLogger(__name__)


class AuthenticationForm(AuthenticationForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Email',
    }), label=_("Email"), max_length=300)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
    }), label=_("Password"))
    game_slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self, *args, **kwargs):
        super(AuthenticationForm, self).clean(*args, **kwargs)
        try:
            UserProfilePerInstance.objects.get(
                        instance__slug=self.cleaned_data.get('game_slug'),
                        user_profile__user__email=self.cleaned_data.get('username', '')
            )
        except UserProfilePerInstance.DoesNotExist:
            raise forms.ValidationError(_("You have not registered for this instance."))

        return self.cleaned_data


class RegistrationForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First Name',
    }), required=True, max_length=30, label=_("First Name"))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last Name'
    }), required=True, max_length=30, label=_("Last Name"))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Email Address',
    }), max_length=75, label=_(u'Email Address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
    }, render_value=False), label=_(u'Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }, render_value=False), label=_(u'Confirm Password'))
    game_slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in ``non_field_errors()`` 
        because it doesn't apply to a single field.
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']

    class Meta:
        model = UserProfilePerInstance
        exclude = (
                'instance',
                'user_profile',
                'stake',
                'stakes',
                'affils',
                'comments',
                'date_created'
        )


class DemographicForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(DemographicForm, self).__init__(*args, **kwargs)
        self.current_game = kwargs['initial'].get('current_game')
        ['current_game']
        self.fields['avatar'] = forms.ImageField(required=False)

        try:
            variants = self.current_game.user_profile_variants
        except UserProfileVariantsForInstance.DoesNotExist:
            stakes = UserProfileStake.objects.none()
            affiliations = UserProfileStake.objects.none()
        else:
            stakes = variants.stake_variants.all().order_by("pos")
            affiliations = variants.affiliation_variants.all().order_by("name")

        self.fields['stakes'] = forms.ModelMultipleChoiceField(
                                    label=_(u'Stake in the community'),
                                    required=False,
                                    queryset=stakes,
        )
        self.fields['affiliations'] = forms.ModelMultipleChoiceField(
                                    label=_(u'Affiliations'),
                                    required=False,
                                    queryset=affiliations,
        )
        self.fields['affiliations_other'] = forms.CharField(required=False, 
               label=_("Don't see your affiliation? Enter it here. Please place a comma between each affiliation."))



class ForgotForm(forms.Form):
    email = forms.EmailField()

    # Ensure that the email address is in the system otherwise no need to send a password reset.
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            return email
        except User.DoesNotExist:
            raise forms.ValidationError(_('Email not found in our system'))

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}))

    # Ensure that both passwords match.
    def clean_confirm(self):
        password = self.cleaned_data['password']
        confirm = self.cleaned_data['confirm']
        if not password == confirm:
            raise forms.ValidationError(_('Passwords must match'))

        return confirm


class UserProfileForm(forms.ModelForm):
    # Required fields
    receive_email = forms.BooleanField(required=False, label=_('Receive notifications via email'))
    tagline = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Give yourself a tagline...'}), required=False, label=_('Tagline'))
    affiliation_new = forms.CharField(
                max_length=100, required=False, label=_("Don't see an affiliation that fits you?"),
                widget=forms.TextInput(attrs={"placeholder": "Add your own Affiliation"})
    )
    avatar = forms.ImageField(required=False)

    stakes = forms.ModelMultipleChoiceField(
                        label=_(u'Stake in the community'),
                        widget= FilteredSelectMultiple("Stakes", False, attrs={'rows':'10'}),
                        queryset = UserProfileStake.objects.none(),
                        required=False,
    )
    affiliations = forms.ModelMultipleChoiceField(
                        label=_(u'Affiliations'),
                        widget= FilteredSelectMultiple("Affiliations", False, attrs={'rows':'10'}),
                        queryset = Affiliation.objects.none(),
                        required=False,
    )


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')

        super(UserProfileForm, self).__init__(*args, **kwargs)

        lang_qs = Language.objects.filter(instance=self.request.current_game)
        if lang_qs.count()  > 1:
            self.fields['preferred_language'] = forms.ModelChoiceField(required=True, 
                                                    label=_("Preferred Language"), 
                                                    queryset=lang_qs,
            )
        self.fields['stakes'].queryset = self.request.current_game.user_profile_variants.stake_variants.all().order_by("pos")
        self.fields['affiliations'].queryset = self.request.current_game.user_profile_variants.affiliation_variants.all().order_by("name")

    class Meta:
        fields = ('receive_email', 'tagline', 'avatar', 'stakes', 'affiliations')
        model = UserProfile


class FilterPlayersByVariantsForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super(FilterPlayersByVariantsForm, self).__init__(*args, **kwargs)
        if not request:
            raise RuntimeError("request obj is missing")
        self.request = request
        qs = UserProfileVariantsForInstance.objects.get(instance=request.current_game)
        stakes_qs = qs.stake_variants.language(get_language()).all().order_by('stake')
        self.fields['stakes'] = forms.ModelChoiceField(label=_("Stakes"), required=False, queryset=stakes_qs, empty_label="Stakes")

        affiliations_qs = qs.affiliation_variants.all().order_by('name')
        self.fields['affiliation'] = forms.ModelChoiceField(label=_("Affiliations"), required=False, queryset=affiliations_qs, empty_label="Affiliations")

    def search(self):
        cd = self.cleaned_data
        qs =  UserProfilePerInstance.objects.filter(instance=self.request.current_game)
        if cd.get('stakes') is not None and cd.get('stakes') != '':
            qs = qs.filter(stakes=cd.get('stakes'))
        if cd.get('affiliation') is not None and cd.get('affiliation') != '':
            qs = qs.filter(affils=cd.get('affiliation'))
        return qs.exclude(user_profile__user__is_active=False)


class SearchPlayersByKeywordsForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super(SearchPlayersByKeywordsForm, self).__init__(*args, **kwargs)
        if not request:
            raise RuntimeError("request obj is missing")
        self.request = request
        self.fields['q'] = forms.CharField(label=_("Keywords"), max_length=50)

    def search(self):
        qs =  UserProfilePerInstance.objects.filter(
                            instance=self.request.current_game
        )
        cd = self.cleaned_data
        if cd.get('q') != '':
            qs = qs.filter(
                    Q(user_profile__user__first_name__icontains = cd.get('q')) |
                    Q(user_profile__user__last_name__icontains = cd.get('q'))
            )
        return qs.exclude(user_profile__user__is_active=False)


class AdminInstanceEmailForm(forms.Form):
    subject = forms.CharField()
    email = forms.CharField(widget=forms.Textarea(attrs={"rows": 6, "cols": 40}))


# Passwords
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import get_template, render_to_string
from django.contrib.sites.models import get_current_site
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.utils.http import int_to_base36

class PasswordResetForm(PasswordResetForm):
    '''
    A Password Reset form for sending out HTML emails
    '''
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}))

    # override django.contrib.auth.form.PasswordResetForm's default save method to allow HTML emails.
    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            # Email subject *must not* contain newlines
            subject = 'Password Reset Requested with %s' % site_name
            from_email = ''
            to = [user.email,]
            message = ''
            html_template = render_to_string(email_template_name, c)
            email = EmailMultiAlternatives(subject, message, from_email, to)
            email.attach_alternative(html_template, "text/html")
            email.send()

class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm New Password'}))

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Current Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm New Password'}))
    
