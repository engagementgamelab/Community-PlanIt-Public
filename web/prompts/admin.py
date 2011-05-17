from django.contrib import admin

from web.prompts.basic.models import *
admin.site.register(BasicPrompt, BasicPromptAdmin)

from web.prompts.map.models import *
admin.site.register(MapPrompt, MapPromptAdmin)

from web.prompts.profile.models import *
admin.site.register(ProfilePrompt, ProfilePromptAdmin)
