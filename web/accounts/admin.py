from django.contrib import admin

from nani.admin import TranslatableAdmin

from web.accounts.models import *

class UserProfileOptionAdmin(TranslatableAdmin):
    list_display = ('__str__', 'instance', 'pos', 'all_translations')

admin.site.register(UserProfile)
admin.site.register(UserProfileEducation, UserProfileOptionAdmin)
admin.site.register(UserProfileGender, UserProfileOptionAdmin)
admin.site.register(UserProfileHowDiscovered, UserProfileOptionAdmin)
admin.site.register(UserProfileIncome, UserProfileOptionAdmin)
admin.site.register(UserProfileLivingSituation, UserProfileOptionAdmin)
admin.site.register(UserProfileRace, UserProfileOptionAdmin)
admin.site.register(UserProfileStake, UserProfileOptionAdmin)
