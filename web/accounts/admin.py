from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import *
from .actions import export_emails_for_instance_csv

admin.site.unregister(User)
admin.site.unregister(Group)

from django import forms
from django.utils.safestring import mark_safe

class AdminImageWidget(forms.FileInput):
    """
    A ImageField Widget for admin that shows a thumbnail.
    """

    def __init__(self, attrs={}):
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a target="_blank" href="%s">'
                           '<img src="%s" style="height: 100px;" /></a> '
                           % (value.url, value.url)))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class UserProfileOptionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pos', 'all_translations')


class UserProfileStakeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileStake, UserProfileStakeAdmin)


class UserProfileIncomeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileIncome, UserProfileIncomeAdmin)


class UserProfileGenderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileGender, UserProfileGenderAdmin)


class UserProfileEducationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileEducation, UserProfileEducationAdmin)


class UserProfileLivingSituationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileLivingSituation, UserProfileLivingSituationAdmin)


class UserProfileRaceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileRace, UserProfileRaceAdmin)


class UserProfileHowDiscoveredAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileHowDiscovered, UserProfileHowDiscoveredAdmin)


#class UserProfilePerInstanceAdmin(admin.ModelAdmin):
#    list_display = ('__str__', 'date_created',)
#    list_filter = ('instance', 'date_created',)
#    search_fields = ('user_profile__email',)
#    actions = [export_emails_for_instance_csv]
#admin.site.register(UserProfilePerInstance, UserProfilePerInstanceAdmin)


class UserProfilePerInstanceInline(admin.StackedInline):
    model = UserProfile.instances.through
    #filter_horizontal = ('stakes', 'affils',)
    readonly_fields = ('stakes', 'affils',)
    extra = 0


class GameListFilter(admin.SimpleListFilter):
    title = 'games'
    parameter_name = 'game'

    def lookups(self, request, model_admin):
        return Instance.objects.values_list('pk', 'title')

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(instances__pk=self.value()).distinct()
        return queryset


class ProfileForm(forms.ModelForm):

    first_name = forms.CharField(max_length=256)
    last_name = forms.CharField(max_length=256)
    avatar_thumb = forms.ImageField(label=_('Avatar'), required=False, widget=AdminImageWidget)
    email = forms.EmailField(label=_("E-mail"), max_length=75)
    last_login = forms.DateTimeField()
    date_joined = forms.DateTimeField()
    is_active = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['avatar_thumb'].initial = self.instance.avatar
            self.fields['last_login'].initial = self.instance.user.last_login
            self.fields['last_login'].widget.attrs['readonly'] = True
            self.fields['date_joined'].initial = self.instance.user.date_joined
            self.fields['date_joined'].widget.attrs['readonly'] = True
            self.fields['is_active'].initial = self.instance.user.is_active

            if self.instance.user.email:
                self.fields['email'].initial = self.instance.user.email
            else:
                self.fields['email'].initial = self.instance.email
        except User.DoesNotExist:
            pass

    class Meta:
        model = UserProfile
        exclude = ('mission_states', 'user',)
        fields = [
            'first_name', 
            'last_name', 
            'avatar_thumb',
            'last_login',
            'date_joined',

            'receive_email',
            'city',
            'zip_code',
            'birth_year', 
            'gender',
            'race',
            'education',
            'income',
            'living',
            'how_discovered',
            'how_discovered_other',
            'tagline',
        ]


class UserProfileAdmin(admin.ModelAdmin):

    form = ProfileForm

    fieldsets = (
        (_('User Info'), {
            'fields': ('first_name', 'last_name', 'email',)
        }),
        (_('Demographic Data'), {
            'classes': ('collapse',),
            'fields': (
                'city',
                'zip_code',
                'birth_year',
                'gender',
                'race',
                'education',
                'income',
                'living',
                'how_discovered',
                'how_discovered_other',
            )
        }),
        (_('User Info Misc'), {
            'classes': ('collapse',),
            'fields': ('receive_email', 'avatar_thumb', 'tagline',)
        }),
        (_('Permissions'), 
            {'fields': ('is_active',)}
        ),
        (_('Important dates'), 
            {'classes': ('collapse',),
             'fields': ('last_login', 'date_joined')}
        ),
    )
    list_display = ('user_first_name', 'user_last_name', 'user_email')
    list_filter = (GameListFilter,)
    search_fields = ('email',)
    inlines = [UserProfilePerInstanceInline,]

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = _("Last Name")

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = _("First Name")

    def user_email(self, obj):
        return obj.email or obj.user.email
    user_email.short_description = _("E-Mail")

    def save_model(self, request, obj, form, change):
        obj.user.first_name = form.cleaned_data['first_name']
        obj.user.last_name = form.cleaned_data['last_name']
        obj.user.email = form.cleaned_data['email']
        obj.user.is_active = form.cleaned_data['is_active']
        obj.user.save()
        obj.avatar = form.cleaned_data['avatar_thumb']
        #TODO why does UserProfile have the email field?
        obj.email = form.cleaned_data['email']
        obj.save()

admin.site.register(UserProfile, UserProfileAdmin)



