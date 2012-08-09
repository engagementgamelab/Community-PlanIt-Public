#from mptt.admin import MPTTModelAdmin
#from django.contrib import admin

#from web.missions.models import Mission
#from web.challenges.models import Challenge

#class ChallengesInline(admin.StackedInline):
#	model = Challenge


#class MissionAdmin(MPTTModelAdmin):
#    list_display = ('title', 'instance', 'start_date', 'end_date')
    #readonly_fields = ('start_date', 'end_date',)
#    list_filter = ('instance', 'instance__city')
#    inlines = [ChallengesInline,]

#admin.site.register(Mission, MissionAdmin)


