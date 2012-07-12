from sijax import Sijax
from localeurl.utils import strip_path

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
from web.instances.models import Instance, City, Language, Affiliation

from web.core.utils import get_translation_with_fallback

import logging
log = logging.getLogger(__name__)


class RegisterFormOne(forms.Form):

    first_name = forms.CharField(required=True, max_length=30, label=_("First Name"))
    last_name = forms.CharField(required=True, max_length=30, label=_("Last Name"))
    email = forms.EmailField(required=True, label=_("Email"))
    password = forms.CharField(required=True, label=_("Password"), widget=forms.PasswordInput(render_value=False))
    password_again = forms.CharField(required=True, label=_("Password Again"), widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        domain = None
        if 'domain' in kwargs:
            self.domain = kwargs.pop('domain')
        super(RegisterFormOne, self).__init__(*args, **kwargs)

        instances = ()
        try:
            current_city = City.objects.get(domain=self.domain)
            self.fields['city'] = forms.CharField(widget=forms.HiddenInput(), initial=current_city.pk)
        except City.DoesNotExist:
            cities = City.objects.values_list('pk', 'name')
            self.fields['city'] = forms.ChoiceField(label=_('Choose your city'), choices=cities)
        self.fields['instance'] = forms.ModelChoiceField(label=_(u'Select your game'), required=False, queryset=Instance.objects.exclude(is_disabled=True).all())
        self.fields['preferred_language'] = forms.ModelChoiceField(required=True, 
                                                            label=_("Preferred Language"), 
                                                            queryset=Language.objects.all()
        )

    def clean(self):
        """Ensure that a user has not already registered an account with that email address and that game."""
        if ('email', 'instance') in self.cleaned_data.items():
            qs = UserProfilePerInstance.objects.filter(
                        user_profile__email=self.cleaned_data['email'], 
                        instance=self.cleaned_data['instance'])
            if qs.count() != 0:
                raise forms.ValidationError(_('Account already exists for this game, please use a different email address.'))
        return self.cleaned_data

    def clean_password_again(self):
        password_again = self.cleaned_data['password_again']
        if (password_again != self.cleaned_data['password']):
            raise forms.ValidationError(_('The passwords do not match.'))
        return password_again
    
class RegisterFormTwo(forms.Form):

    def __init__(self, *args, **kwargs):
        chosen_game = None
        if 'chosen_game' in kwargs:
            chosen_game = kwargs.pop('chosen_game')
        super(RegisterFormTwo, self).__init__(*args, **kwargs)
        self.chosen_game = chosen_game
        self.fields['avatar'] = forms.ImageField(required=False)

        # TODO need to figure out a way of displaying the 
        # current language stakes with a way to include the default
        # language as well
        self.fields['stakes'] = forms.ModelMultipleChoiceField(
                                    label=_(u'Stake in the community'),
                                    required=False,
                                    queryset=self.chosen_game.user_profile_variants.\
                                            stake_variants.language(
                                                    settings.LANGUAGE_CODE
                                            ).all().order_by("pos")
        )
        self.fields['affiliations'] = forms.ModelMultipleChoiceField(
                                    label=_(u'Affiliations'),
                                    required=False,
                                    queryset=self.chosen_game.user_profile_variants.affiliation_variants.all().order_by("name")
        )
        self.fields['affiliations_other'] = forms.CharField(required=False, 
               label=_("Don't see your affiliation? Enter it here. Please place a comma between each affiliation."))

        self.fields['birth_year'] = forms.IntegerField( label=_('Year you were born'), required=False)
        self.fields['zip_code'] = forms.CharField(max_length=10, label=_('Your ZIP code'))


        all_genders = UserProfileGender.objects.untranslated().all().order_by("pos")
        genders = [(0, '------')] + [(x.pk, get_translation_with_fallback(x, 'gender')) for x in all_genders]
        self.fields['gender'] = forms.ChoiceField(label=_(u'Gender'), required=False, choices=genders)
        all_races = UserProfileRace.objects.untranslated().all().order_by("pos")
        races = [(0, '------')] + [(x.pk, get_translation_with_fallback(x, 'race')) for x in all_races]
        self.fields['race'] = forms.ChoiceField(label=_(u'Race/Ethnicity'), required=False, choices=races)

        all_educations = UserProfileEducation.objects.untranslated().all().order_by("pos")
        educations = [(0, '------')] + [(x.pk, get_translation_with_fallback(x, 'education')) for x in all_educations]
        self.fields['education'] = forms.ChoiceField(label=_(u'Education'), required=False, choices=educations)

        all_incomes = UserProfileIncome.objects.untranslated().all().order_by("pos")
        incomes = [(0, '------')] + [(x.pk, get_translation_with_fallback(x, 'income')) for x in all_incomes]
        self.fields['income'] = forms.ChoiceField(label=_(u'Household Income'), required=False, choices=incomes)
        
        all_livings = UserProfileLivingSituation.objects.untranslated().all().order_by("pos")
        livings = [(0, '------')] + [(x.pk, get_translation_with_fallback(x, 'situation')) for x in all_livings]
        self.fields['living'] = forms.ChoiceField(label=_(u'Living Situation'), required=False, choices=livings)

        all_hows = UserProfileHowDiscovered.objects.untranslated().all().order_by("pos")
        hows = [(0, '------')] + [(x.pk, get_translation_with_fallback(x, 'how')) for x in all_hows]
        self.fields['how_discovered'] = forms.ChoiceField(label=_(u'How did you hear about Community PlanIt?'), required=False, choices=hows)

        self.fields['how_discovered_other'] = forms.CharField(
            required=False, 
            max_length=1000,
            label=_('If other, please tell us how you learned about Community PlanIt'),
            widget=forms.Textarea())

        self.fields['tagline'] = forms.CharField(
            required=False, 
            max_length=140,
            label=_('Give yourself a tagline'),
            widget=forms.Textarea(attrs={"placeholder": "I'm here to..."}))


    def clean_gender(self):
        try:
            return UserProfileGender.objects.get(pk=self.cleaned_data['gender'])
        except UserProfileGender.DoesNotExist:
            return None
    
    def clean_education(self):
        try:
            return UserProfileEducation.objects.get(pk=self.cleaned_data['education'])
        except UserProfileEducation.DoesNotExist:
            return None
    
    def clean_how_discovered(self):
        try:
            return UserProfileHowDiscovered.objects.get(pk=self.cleaned_data['how_discovered'])
        except UserProfileHowDiscovered.DoesNotExist:
            return None
    
    def clean_income(self):
        try:
            return UserProfileIncome.objects.get(pk=self.cleaned_data['income'])
        except UserProfileIncome.DoesNotExist:
            return None
    
    def clean_living(self):
        try:
            return UserProfileLivingSituation.objects.get(pk=self.cleaned_data['living'])
        except UserProfileLivingSituation.DoesNotExist:
            return None
        
    def clean_race(self):
        try:
            return UserProfileRace.objects.get(pk=self.cleaned_data['race'])
        except UserProfileRace.DoesNotExist:
            return None


class RegistrationWizard(SessionWizardView):
    __name__ = 'RegistrationWizard'

    #def dispatch(self, request, *args, **kwargs):
    #    response = super(RegistrationWizard, self).dispatch(request, *args, **kwargs)
    #    if self.request.user.is_authenticated():
    #        return redirect(reverse('accounts:dashboard'), permanent=True)
    #    return response

    #def get_form(self, step=None, data=None, files=None):
    #    data = {'request': self.request}
    #    form = super(RegistrationWizard, self).get_form(step, data, files)
    #    return form

    def __init__(self, *args, **kwargs):
        super(RegistrationWizard, self).__init__(*args, **kwargs)
        self.file_storage = FileSystemStorage()

    def get_form_kwargs(self, step=None):
        if step == '1':
            #TODO is there another way to get
            #TODO to the data of the previous steps data
            chosen_game_id = self.storage.data.get('step_data')['0']['0-instance'][0]

            try:
                chosen_game = Instance.objects.language(get_language()).get(id=chosen_game_id)
            except Instance._meta.translations_model.DoesNotExist:
                chosen_game = Instance.objects.language(settings.LANGUAGE_CODE).get(id=chosen_game_id)

            return {'chosen_game' : chosen_game}
        if step == '0':
            return {'domain' : self.request.current_site.domain}
        return {}

    def get_context_data(self, form, **kwargs):
        context = super(RegistrationWizard, self).get_context_data(form, **kwargs)

        self.template_name = 'accounts/register_%s.html' % self.steps.current
        if self.steps.current == '0':
            load_games_sijax = Sijax()
            load_games_uri = reverse('instances:ajax-load-games-by-city', args=(1,))
            load_games_sijax.set_request_uri(load_games_uri)

            login_sijax = Sijax()
            login_sijax.set_request_uri(reverse('accounts:login-ajax'))
            self.request.session.set_test_cookie()

            context.update(
                    dict(
                        load_games_sijax_js = load_games_sijax.get_js(),
                        login_sijax_js = login_sijax.get_js(),
                        form = AccountAuthenticationForm(self.request),
                    )
            )
        elif self.steps.current == '1':
            chosen_game_id = self.storage.data.get('step_data')['0']['0-instance'][0]
            try:
                chosen_game = Instance.objects.language(get_language()).get(id=chosen_game_id)
            except Instance._meta.translations_model.DoesNotExist:
                chosen_game = Instance.objects.language(settings.LANGUAGE_CODE).get(id=chosen_game_id)
            context.update( {'chosen_game' : chosen_game})

        return context

    @transaction.commit_on_success
    def done(self, form_list):
        form_one = form_list[0]
        form_two = form_list[1]

        log.debug(form_one.cleaned_data)
        log.debug(form_two.cleaned_data)

        game = form_one.cleaned_data.get('instance')

        first_name = form_one.cleaned_data.get('first_name')
        last_name = form_one.cleaned_data.get('last_name')
        email = form_one.cleaned_data.get('email')
        password = form_one.cleaned_data.get('password')

        player, created = User.objects.get_or_create(email=email)
        player.first_name=first_name
        player.last_name=last_name
        player.is_active=True
        player.set_password(password)
        player.save()

        player = authenticate(username=email, password=password)
        login(self.request, player)
        player.save()

        profile = player.get_profile()
        profile.email = form_one.cleaned_data.get('email')
        profile.city = form_one.cleaned_data.get('city')

        profile.avatar = form_two.cleaned_data.get('avatar')

        birth_year = form_two.cleaned_data.get('birth_year')
        if birth_year:
            profile.birth_year = birth_year
        profile.zip_code = form_two.cleaned_data.get('zip_code')
        profile.education = form_two.cleaned_data.get('education')
        profile.gender = form_two.cleaned_data.get('gender')
        profile.income = form_two.cleaned_data.get('income')
        profile.living = form_two.cleaned_data.get('living')

        profile.race = form_two.cleaned_data.get('race')
        profile.how_discovered = form_two.cleaned_data.get('how_discovered')
        profile.how_discovered_other = form_two.cleaned_data.get('how_discovered_other')
        profile.tagline = form_two.cleaned_data.get('tagline')

        profile.save()

        user_profile_per_instance = UserProfilePerInstance(
                                        user_profile=profile,
                                        instance=game,
                                        preferred_language = form_one.cleaned_data.get('preferred_language'),
                )
        user_profile_per_instance.save()

        user_profile_per_instance.affils = form_two.cleaned_data.get('affiliations')
        user_profile_per_instance.stakes = form_two.cleaned_data.get('stakes')

        aff_other = form_two.cleaned_data.get('affiliations_other')
        if aff_other != '':
            for a in aff_other.split(','):
                aff, created = Affiliation.objects.get_or_create(name=a.strip())
                if created:
                    aff.save()
                user_profile_per_instance.affils.add(aff)
                variants = UserProfileVariantsForInstance.objects.get(instance=game)
                variants.affiliation_variants.add(aff)
        user_profile_per_instance.save()

        tmpl = loader.get_template('accounts/email/welcome.html')
        context = { 'instance': game }
        body = tmpl.render(RequestContext(self.request, context))
        send_mail(ugettext('Welcome to Community PlanIt!'), body, settings.NOREPLY_EMAIL, [email], fail_silently=False)
        messages.success(self.request, _("Thanks for signing up!"))


        # set the game we are logging the user into
        #
        self.request.session['current_game_slug'] = game.slug
        return redirect(
                os.path.join(
                            'https://' if settings.DEBUG == False else 'http://',
                            game.for_city.domain,
                            user_profile_per_instance.preferred_language.code,
                            strip_path(reverse('accounts:dashboard'))[1][1:],
                )
        )


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


class AccountAuthenticationForm(AuthenticationForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    def __init__(self, request, *args, **kwargs):
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        if not request:
            raise RuntimeError("request obj is missing")
        self.fields['username'] = forms.CharField(label=_("Email"), max_length=300)

        #games_for_domain = Instance.objects.for_city(request.current_site.domain)

        #if games_for_domain.count():
        #    self.fields['instance'] = forms.ModelChoiceField(queryset=games_for_domain)
        #else:

        queryset=Instance.objects.exclude(is_disabled=True)
        if hasattr(request, 'current_city') and request.current_city is not None:
            queryset = queryset.filter(for_city=request.current_city)
        self.fields['instance'] = forms.ModelChoiceField(label=_("Select your game"), queryset=queryset)

    def clean(self, *args, **kwargs):
        super(AccountAuthenticationForm, self).clean(*args, **kwargs)
        try:
            UserProfilePerInstance.objects.get(
                        instance=self.cleaned_data.get('instance'),
                        user_profile__user__email=self.cleaned_data.get('username', '')
            )
        except UserProfilePerInstance.DoesNotExist:
            raise forms.ValidationError(_("You have not registered for this instance."))

        return self.cleaned_data

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
    