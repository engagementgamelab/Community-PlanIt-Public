from web.player_activities.models import PlayerActivity, PlayerActivityType, PlayerActivityAdmin, PlayerActivityTypeAdmin
from django.contrib import admin

# Register to admin sites
admin.site.register(PlayerActivity, PlayerActivityAdmin)
admin.site.register(PlayerActivityType, PlayerActivityTypeAdmin)
admin.site.register(MultiChoiceActivity, MultiChoiceActivityAdmin)
admin.site.register(PlayerMapActivity, PlayerMapActivityAdmin)
admin.site.register(PlayerEmpathyActivity, PlayerEmpathyActivityAdmin)
