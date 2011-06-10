from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from web.instances.models import Instance
from web.accounts.models import UserProfile
from web.accounts.models import UserProfileEducation
from web.accounts.models import UserProfileIncomes
from web.accounts.models import UserProfileLiving

class RegisterForm(forms.Form):
    firstName = forms.CharField(required=True, max_length=30, label=_("First Name"))
    lastName = forms.CharField(required=True, max_length=30, label=_("Last Name"))
    email = forms.EmailField(required=True, label=_("Email:"))
    password = forms.CharField(required=True, label=_("Password"), widget=forms.PasswordInput(render_value=False))
    passwordAgain = forms.CharField(required=True, label=_("Password Again"), widget=forms.PasswordInput(render_value=False))
    instance = forms.ModelChoiceField(queryset=Instance.objects.all(), required=False, label=_('Community'))

    # Ensure that a user has not already registered an account with that email address.
    def clean_email(self):
        email = self.cleaned_data['email']
        if (User.objects.filter(email=email).count() != 0):
            raise forms.ValidationError(_('Account already exists, please use a different email address.'))
        else:
            return email
    
    def clean_firstName(self):
        firstName = self.cleaned_data['firstName']
        if (len(firstName.strip()) == 0):
            raise forms.ValidationError(_('Please provide your first name.'))
        else:
            return firstName
        
    def clean_lastName(self):
        lastName = self.cleaned_data['lastName']
        if (len(lastName.strip()) == 0):
            raise forms.ValidationError(_('Please provide your last name.'))
        else:
            return lastName
        
    def clean_password(self):
        password = self.cleaned_data['password']
        if (len(password.strip()) == 0):
            raise forms.ValidationError(_('Please provide a password.'))
        else:
            return password
    
    def clean_passwordAgain(self):
        passwordAgain = self.cleaned_data['passwordAgain']
        if (len(passwordAgain.strip()) == 0):
            raise forms.ValidationError(_('Please type the password again.'))
        if (passwordAgain != self.cleaned_data['password']):
            raise forms.ValidationError(_('The passwords do not match.'))
        else:
            return passwordAgain
    
class ActivationForm(forms.Form):
    accepted_term = forms.BooleanField(required=True, label=_("I have have read the <a href=\"/label/\">Terms of Use.</a>"))
    accepted_research = forms.BooleanField(required=True, label=_("Accepted research"))

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
    first_name = forms.CharField(max_length=30, required=True,)
    last_name = forms.CharField(max_length=30, required=True,)
    email = forms.CharField(max_length=255, required=True, help_text="(Private)",)

    # Non-required fields
    gender = forms.ChoiceField(required=False, help_text='(Private)', choices=(('', '------'), ('male','Male'), ('female', 'Female'), ('other', 'Other')))
    race = forms.ChoiceField(required=False, help_text='<em class="fine">(Private)</em>', choices=(
        ('','------'), ('asian','Asian'), ('american indian or alaska native','American Indian or Alaska Native'), ('black or african american', 'Black or African American'),
        ('hispanic or latino or spanish','Hispanic, Latino, or Spanish'), ('pacific islander or native hawaiian', 'Pacific Islander or Native Hawaiian'), ('white','White'),
        ('multiracial', 'Multiracial'), ('other','Other')))
    stake = forms.ChoiceField(required=False, choices=(('','------'), ('live','Live'), ('work','Work'), ('play', 'Play')))
    birth_year = forms.CharField(max_length=30, label='Age', help_text='Private',required=False)
    phone_number = forms.CharField(max_length=30, help_text='Private',required=False)
    myInstance = forms.ModelChoiceField(queryset=Instance.objects.all(), required=False, label=_('Community'))
    affiliations = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2, "cols": 40}), 
                                   help_text = "Please place a comma between each affiliation (ie: YMCA, James Memorial Highschool, Gardening Club).")
    c1 = []
    c1.append((0, '------'))
    for x in UserProfileEducation.objects.all().order_by("pos"):
        c1.append((x.id, x.eduLevel))
    education = forms.ChoiceField(required=False, choices=c1)
    
    c2 = []
    c2.append((0, '------'))
    for x in UserProfileIncomes.objects.all().order_by("pos"):
        c2.append((x.id, x.income))
    income = forms.ChoiceField(required=False, choices=c2)
    
    c3 = []
    c3.append((0, '------'))
    for x in UserProfileLiving.objects.all().order_by("pos"):
        c3.append((x.id, x.livingSituation))
    living = forms.ChoiceField(required=False, choices=c3)
    
    avatar = forms.ImageField(required=False)
    
    def clean_email(self):
        email = self.cleaned_data['email']
        return email
    
    class Meta:
        model = UserProfile
        #Adding to Meta.fields will display default settings in the browser and link it to the correct model object. 
        fields = ( 'email', 'first_name', 'last_name', 'stake', 'birth_year', 'gender', 'race', 'phone_number', 'myInstance', 'affiliations', )
