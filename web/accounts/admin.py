from django.contrib import admin

from nani.admin import TranslatableAdmin

from accounts.models import *

class UserProfileOptionAdmin(TranslatableAdmin):
    list_display = ('__str__', 'pos', 'all_translations')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    search_fields = ('email',)
admin.site.register(UserProfile, UserProfileAdmin)

class UserProfileStakeAdmin(TranslatableAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileStake, UserProfileStakeAdmin)

class UserProfileIncomeAdmin(TranslatableAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileIncome, UserProfileIncomeAdmin)

class UserProfileGenderAdmin(TranslatableAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileGender, UserProfileGenderAdmin)

class UserProfileEducationAdmin(TranslatableAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileEducation, UserProfileEducationAdmin)


class UserProfileLivingSituationAdmin(TranslatableAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileLivingSituation, UserProfileLivingSituationAdmin)

class UserProfileRaceAdmin(TranslatableAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileRace, UserProfileRaceAdmin)

class UserProfileHowDiscoveredAdmin(TranslatableAdmin):
    list_display = ('__str__', 'pos')
admin.site.register(UserProfileHowDiscovered, UserProfileHowDiscoveredAdmin)

class UserProfilePerInstanceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_created',)
    list_filter = ('instance', 'date_created',)
    search_fields = ('user_profile__email',)

admin.site.register(UserProfilePerInstance, UserProfilePerInstanceAdmin)

