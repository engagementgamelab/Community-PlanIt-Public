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
    list_display = ('__str__', )
admin.site.register(UserProfileStake, UserProfileStakeAdmin)

class UserProfilePerInstanceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_created',)
    list_filter = ('instance', 'date_created',)
    search_fields = ('user_profile__email',)

admin.site.register(UserProfilePerInstance, UserProfilePerInstanceAdmin)

