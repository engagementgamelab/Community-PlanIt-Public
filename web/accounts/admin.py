from django.contrib import admin

from nani.admin import TranslatableAdmin

from accounts.models import *

class UserProfileOptionAdmin(TranslatableAdmin):
    list_display = ('__str__', 'pos', 'all_translations')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    search_fields = ('email',)

admin.site.register(UserProfile, UserProfileAdmin)

class UserProfilePerInstanceAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    list_filter = ('instance',)

admin.site.register(UserProfilePerInstance, UserProfilePerInstanceAdmin)

