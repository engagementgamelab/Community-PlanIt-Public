from django.contrib import admin
from web.accounts.models import UserProfile

# Augmentation occurs in the UserProfileAdmin, need to unregister the existing
# Django Auth UserAdmin and register the custom ProfileAdmin.
#admin.site.unregister(User)
#admin.site.register(User, UserProfileAdmin)
admin.site.register(UserProfile)
