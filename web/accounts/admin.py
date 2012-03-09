from django.contrib import admin

from nani.admin import TranslatableAdmin

from accounts.models import *

class UserProfileOptionAdmin(TranslatableAdmin):
    list_display = ('__str__', 'pos', 'all_translations')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    search_fields = ('email',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserProfileEducation, UserProfileOptionAdmin)
admin.site.register(UserProfileGender, UserProfileOptionAdmin)
admin.site.register(UserProfileHowDiscovered, UserProfileOptionAdmin)
admin.site.register(UserProfileIncome, UserProfileOptionAdmin)
admin.site.register(UserProfileLivingSituation, UserProfileOptionAdmin)
admin.site.register(UserProfileRace, UserProfileOptionAdmin)
admin.site.register(UserProfileStake, UserProfileOptionAdmin)


class UserProfilePerInstanceAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    list_filter = ('instance',)

admin.site.register(UserProfilePerInstance, UserProfilePerInstanceAdmin)

