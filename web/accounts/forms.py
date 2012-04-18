from sijax import Sijax
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.db import transaction
from django.template import Context, RequestContext, loader
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, ugettext, ugettext_lazy as _

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
#from django.contrib.formtools.wizard import FormWizard
#from django.views.generic.base import TemplateResponseMixin
from django.contrib.formtools.wizard.views import SessionWizardView
#from django.contrib.sites.models import RequestSite

from web.accounts.models import *
from web.instances.models import Instance, City, Language

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
            instances = Instance.objects.exclude(is_disabled=True).filter(for_city=current_city).values_list('pk', 'title') #.distinct().order_by('title')
        except City.DoesNotExist:
            cities = City.objects.values_list('pk', 'name')
            self.fields['city'] = forms.ChoiceField(label=_('Choose your city'), choices=cities)
            #games_for_first_city = Instance.objects.filter(for_city__pk=cities[0][0]).language(get_language())
            #instances = [(x.pk, get_translation_with_fallback(x, 'title')) for x in games_for_first_city]
            instances = Instance.objects.filter(for_city__pk=cities[0][0]).values_list('pk', 'title').distinct().order_by('title')

#        self.fields['instance'] = forms.ChoiceField(label=_(u'Select your game'), required=False, choices=instances)
        self.fields['instance'] = forms.ModelChoiceField(label=_(u'Select your game'), required=False, queryset=Instance.objects.all())
        self.fields['preferred_language'] = forms.ModelChoiceField(required=True, 
                                                            label=_("Preferred Language"), 
                                                            queryset=Language.objects.all()
        )


        #self.fields['accepted_terms'] = forms.BooleanField(
        #    required=True,
        #    label=mark_safe(
        #        _('Confirm that you have read and agree to the <a target="_blank" href="%(terms)s">Terms of Use</a>.') % {'terms': reverse('terms')}
        #    )
        #)

    def clean(self):
        """Ensure that a user has not already registered an account with that email address and that game."""
        if ('email', 'instance') in self.cleaned_data.items():
            if UserProfilePerInstance.objects.filter(
                        user_profile__email=self.cleaned_data['email'], 
                        instance__pk=self.cleaned_data['instance']
                        ).count() != 0:
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
        print self.chosen_game
        print self.chosen_game.user_profile_variants.stake_variants.all()

        #all_stakes = self.chosen_game.user_profile_variants.stake_variants.all().order_by("pos")
        #stakes = [(x.pk, get_translation_with_fallback(x, 'stake')) for x in all_stakes]
        #self.fields['stake'] = forms.ChoiceField(label=_(u'Stake in the community'), required=False, choices=stakes)
        self.fields['stakes'] = forms.ModelMultipleChoiceField(
                                    label=_(u'Stake in the community'),
                                    required=False,
                                    queryset=self.chosen_game.user_profile_variants.stake_variants.all().order_by("pos")
        )

        affiliations = self.chosen_game.user_profile_variants.affiliation_variants.all().order_by('pk', "name").values_list('pk', 'name')
        # self.fields['affiliations'] = forms.MultipleChoiceField(
        #     label=_(u'Affiliation'), required=False, choices=affiliations
        # )
        self.fields['affiliations'] = forms.ChoiceField(
            label=_(u'Affiliation'), required=False, choices=affiliations,
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
            label=_('If other, please tell us how you learned about Community PlanIt'),
            widget=forms.Textarea())

        self.fields['tagline'] = forms.CharField(
            required=False, 
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
    
    #def clean_stakes(self):
    #    try:
    #        return UserProfileStake.objects.get(pk=self.cleaned_data['stake'])
    #    except UserProfileStake.DoesNotExist:
    #        return None


class RegistrationWizard(SessionWizardView):
    __name__ = 'RegistrationWizard'

    def dispatch(self, request, *args, **kwargs):
        response = super(RegistrationWizard, self).dispatch(request, *args, **kwargs)
        if self.request.user.is_authenticated():
            return redirect(reverse('accounts:dashboard'), permanent=True)
        return response

    #def get_form(self, step=None, data=None, files=None):
    #    data = {'request': self.request}
    #    form = super(RegistrationWizard, self).get_form(step, data, files)
    #    return form

    def get_form_kwargs(self, step=None):
        if step == '1':
            #TODO is there another way to get
            #TODO to the data of the previous steps data
            chosen_game_id = self.storage.data.get('step_data')['0']['0-instance'][0]
            chosen_game = Instance.objects.get(id=chosen_game_id)
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
        return context

    @transaction.commit_on_success
    def done(self, form_list):
        form_one = form_list[0]
        form_two = form_list[1]

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
        #profile.instance = self.community
        profile.preferred_language = form_one.cleaned_data['preferred_language']
        profile.city = form_one.cleaned_data.get('city')

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
                        "".join(
                                [
                                    game.get_absolute_url(ssl=not(settings.DEBUG)),
                                    reverse('accounts:dashboard')
                                ]
                            ),
                        permanent=True,
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
    password = forms.CharField(widget=forms.PasswordInput)
    confirm = forms.CharField(widget=forms.PasswordInput)

    # Ensure that both passwords match.
    def clean_confirm(self):
        password = self.cleaned_data['password']
        confirm = self.cleaned_data['confirm']
        if not password == confirm:
            raise forms.ValidationError(_('Passwords must match'))

        return confirm

class UserProfileForm(forms.ModelForm):
    # Required fields
    first_name = forms.CharField(max_length=30, required=True, label=_('First Name'))
    last_name = forms.CharField(max_length=30, required=True, label=_('Last Name'))
    email = forms.CharField(max_length=250, required=True, label=_('Email'))
    receive_email = forms.BooleanField(required=False, label=_('Should we send you notifications and news via email?'))
    preferred_language = forms.ChoiceField(choices=[(l[0], _(l[1])) for l in settings.LANGUAGES], label=_('Preferred Language'))
    avatar = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        #TODO
        # need to include the user selected choices in the list
        #affil_choices = Affiliation.objects.filter(instance=self.instance.instance).order_by("name").values_list('pk', 'name')

        #self.fields['affils'] = forms.MultipleChoiceField(label=_(u'Affiliations'), help_text=_('Right Click (or control and click on a Mac) to select more than one affiliation'), required=False, choices=affil_choices)

        #self.fields['affiliations_other'] = forms.CharField(required=False, 
        #       label=_('Don\'t see your affiliation? Enter it here. Please place a comma between each affiliation.'),
        #        widget=forms.Textarea(attrs={"rows": 2, "cols": 40}))

    class Meta:
        model = UserProfile
        fields = ('email', 'first_name', 'last_name', 'preferred_language',
                  'receive_email', 
                  #'affils'
            )

    def clean_stake(self):
        try:
            return UserProfileStake.objects.get(pk=self.cleaned_data['stake'])
        except UserProfileStake.DoesNotExist:
            return None
    

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
        self.fields['instance'] = forms.ModelChoiceField(label=_("Select your game"), queryset=Instance.objects.all())

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

