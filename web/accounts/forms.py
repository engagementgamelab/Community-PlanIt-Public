from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, ugettext, ugettext_lazy as _

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.formtools.wizard import FormWizard

from django.contrib.sites.models import RequestSite

from accounts.models import *
from instances.models import Instance

from core.utils import get_translation_with_fallback

class RegisterFormOne(forms.Form):

    first_name = forms.CharField(required=True, max_length=30, label=_("First Name"))
    last_name = forms.CharField(required=True, max_length=30, label=_("Last Name"))
    email = forms.EmailField(required=True, label=_("Email"))
    password = forms.CharField(required=True, label=_("Password"), widget=forms.PasswordInput(render_value=False))
    password_again = forms.CharField(required=True, label=_("Password Again"), widget=forms.PasswordInput(render_value=False))
    preferred_language = forms.ChoiceField(label=_("Preferred Language"), choices=settings.LANGUAGES)

    birth_year = forms.IntegerField(label=_('Year you were born'), required=False)

    city = forms.CharField(max_length=128, label=_('Your neighborhood, town or city'))
    zip_code = forms.CharField(max_length=10, label=_('Your ZIP code'))

    def __init__(self, *args, **kwargs):
        super(RegisterFormOne, self).__init__(*args, **kwargs)

        all_instances = Instance.objects.active().language(get_language())
        instances = [(x.pk, get_translation_with_fallback(x, 'title')) for x in all_instances]
        self.fields['instance_id'] = forms.ChoiceField(label=_(u'Community'), required=False, choices=instances)

        self.fields['accepted_terms'] = forms.BooleanField(
            required=True,
            label=mark_safe(
                _('Confirm that you have read and agree to the <a target="_blank" href="%(terms)s">Terms of Use</a>.') % {'terms': reverse('terms')}
            )
        )

    def clean_email(self):
        """Ensure that a user has not already registered an account with that email address."""
        email = self.cleaned_data['email']
        if (User.objects.filter(email=email).count() != 0):
            raise forms.ValidationError(_('Account already exists, please use a different email address.'))
        else:
            return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if (len(first_name.strip()) == 0):
            raise forms.ValidationError(_('Please provide your first name.'))
        else:
            return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if (len(last_name.strip()) == 0):
            raise forms.ValidationError(_('Please provide your last name.'))
        else:
            return last_name

    def clean_password(self):
        password = self.cleaned_data['password']
        if (len(password.strip()) == 0):
            raise forms.ValidationError(_('Please provide a password.'))
        else:
            return password
    
    def clean_password_again(self):
        password_again = self.cleaned_data['password_again']
        if (len(password_again.strip()) == 0):
            raise forms.ValidationError(_('Please type the password again.'))
        if (password_again != self.cleaned_data['password']):
            raise forms.ValidationError(_('The passwords do not match.'))
        else:
            return password_again
    
class RegisterFormTwo(forms.Form):

    def __init__(self, *args, **kwargs):
        community = None
        if 'community' in kwargs:
            community = kwargs.pop('community')
        super(RegisterFormTwo, self).__init__(*args, **kwargs)
        self.community = community

        all_stakes = self.community.user_profile_variants.stake_variants.all().order_by("pos")
        stakes = [(x.pk, get_translation_with_fallback(x, 'stake')) for x in all_stakes]
        self.fields['stake'] = forms.ChoiceField(label=_(u'Stake in the community'), required=False, choices=stakes)

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
        self.fields['income'] = forms.ChoiceField(label=_(u'Income'), required=False, choices=incomes)
        
        all_livings = UserProfileLivingSituation.objects.untranslated().all().order_by("pos")
        livings = [(0, '------')] + [(x.pk, get_translation_with_fallback(x, 'situation')) for x in all_livings]
        self.fields['living'] = forms.ChoiceField(label=_(u'Living Situation'), required=False, choices=livings)


        all_hows = UserProfileHowDiscovered.objects.untranslated().all().order_by("pos")
        hows = [(0, '------')] + [(x.pk, get_translation_with_fallback(x, 'how')) for x in all_hows]
        self.fields['how_discovered'] = forms.ChoiceField(label=_(u'How did you hear about Community PlanIt?'), required=False, choices=hows)

        self.fields['how_discovered_other'] = forms.CharField(required=False, label=_('If the way you learned about us is not listed, please tell us'))


        affiliations = Affiliation.objects.filter(instance=self.community).order_by("name").values_list('pk', 'name')
        self.fields['affiliations'] = forms.MultipleChoiceField(label=_(u'Affiliation'), required=False, choices=affiliations)

        self.fields['affiliations_other'] = forms.CharField(required=False, 
               label=_('Don\'t see your affiliation? Enter it here. Please place a comma between each affiliation.'),
                widget=forms.Textarea(attrs={"rows": 2, "cols": 40}))
        

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
    
    def clean_stake(self):
        try:
            return UserProfileStake.objects.get(pk=self.cleaned_data['stake'])
        except UserProfileStake.DoesNotExist:
            return None


class RegistrationWizard(FormWizard):
    community = None
    __name__ = 'RegistrationWizard'

    @transaction.commit_on_success
    def done(self, request, form_list):
        form_one = form_list[0]
        form_two = form_list[1]

        first_name = form_one.cleaned_data.get('first_name')
        last_name = form_one.cleaned_data.get('last_name')
        email = form_one.cleaned_data.get('email')
        password = form_one.cleaned_data.get('password')

        player = User.objects.create(email=email,first_name=first_name, last_name=last_name, is_active=True)
        player.set_password(password)
        player.save()

        player = authenticate(username=email, password=password)
        login(request, player)
        player.save()

        profile = player.get_profile()
        profile.email = form_one.cleaned_data.get('email')
        #profile.instance = self.community
        profile.preferred_language = form_one.cleaned_data['preferred_language']
        birth_year = form_one.cleaned_data.get('birth_year')
        if birth_year:
            profile.birth_year = birth_year
        profile.city = form_one.cleaned_data.get('city')
        profile.zip_code = form_one.cleaned_data.get('zip_code')

        profile.education = form_two.cleaned_data.get('education')
        profile.gender = form_two.cleaned_data.get('gender')
        profile.income = form_two.cleaned_data.get('income')
        profile.living = form_two.cleaned_data.get('living')

        profile.race = form_two.cleaned_data.get('race')
        profile.how_discovered = form_two.cleaned_data.get('how_discovered')
        profile.how_discovered_other = form_two.cleaned_data.get('how_discovered_other')

        profile.save()

        user_profile_per_instance = UserProfilePerInstance(
                                        user_profile=profile,
                                        instance=self.community,
                )
        user_profile_per_instance.save()

        user_profile_per_instance.affils = form_two.cleaned_data.get('affiliations')
        user_profile_per_instance.stake = form_two.cleaned_data.get('stake')


        aff_other = form_two.cleaned_data.get('affiliations_other')
        if aff_other != '':
            for a in aff_other.split(','):
                aff, created = Affiliation.objects.get_or_create(name=a.strip())
                if created:
                    aff.save()
                user_profile_per_instance.affils.add(aff)
        user_profile_per_instance.save()

        tmpl = loader.get_template('accounts/email/welcome.html')
        context = { 'instance': self.community }
        body = tmpl.render(RequestContext(request, context))
        send_mail(ugettext('Welcome to Community PlanIt!'), body, settings.NOREPLY_EMAIL, [email], fail_silently=False)
        messages.success(request, _("Thanks for signing up!"))
        request.session['instance'] = self.community
        return HttpResponseRedirect(reverse('accounts:dashboard'))

    def get_form(self, step, data=None):
        if step == 0 and data:
            instance_id = data.get('0-instance_id')
            self.community = Instance.objects.get(id=instance_id)

        if step == 1:
            form = self.form_list[step](data,
                                        community=self.community,
                                        prefix=self.prefix_for_step(step),
                                        initial=self.initial.get(step, None)
                                       )
            return form

        return self.form_list[step](data, prefix=self.prefix_for_step(step), initial=self.initial.get(step, None))

    def get_template(self, step):
        return 'accounts/register_%s.html' % step

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
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.site = RequestSite(self.request)
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(label=_("Username"), max_length=300)        

    def clean(self, *args, **kwargs):
        super(AccountAuthenticationForm, self).clean(*args, **kwargs)
        #import ipdb;ipdb.set_trace()
        print "invalid"
        raise forms.ValidationError(_("You have not registered for this instance."))

class AdminInstanceEmailForm(forms.Form):
    subject = forms.CharField()
    email = forms.CharField(widget=forms.Textarea(attrs={"rows": 6, "cols": 40}))

