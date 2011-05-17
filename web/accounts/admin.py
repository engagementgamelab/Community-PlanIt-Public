from django.contrib.auth.models import User
from django.contrib import admin
from web.accounts.models import User, UserProfileAdmin

# Augmentation occurs in the UserProfileAdmin, need to unregister the existing
# Django Auth UserAdmin and register the custom ProfileAdmin.
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
