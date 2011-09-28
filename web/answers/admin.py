from django.contrib import admin

## Games players have completed
#from web.games.models import PlayerGame
#admin.site.register(PlayerGame)
#
## Other shoes
#from web.games.othershoes.models import *
#admin.site.register(OtherShoes, OtherShoesAdmin)
#
## Think Fast!
#from web.games.thinkfast.models import *
#admin.site.register(ThinkFast, ThinkFastAdmin)
#
## MapIt
#from web.games.mapit.models import *
#admin.site.register(Mapit, MapitAdmin)

from web.answers.models import *
admin.site.register(Answer)
admin.site.register(AnswerEmpathy)
admin.site.register(AnswerSingleResponse)
admin.site.register(AnswerOpenEnded)

class AnswerMapAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'activity', 'user_name')
    
    def user_name(self, obj):
        return obj.answerUser.get_profile() and obj.answerUser.get_profile().screen_name or answerUser.answerUsername

admin.site.register(AnswerMap, AnswerMapAdmin)

class AnswerMultiChoiceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'activity', 'user_name')

    def activity(self, obj):
        return unicode(obj.option.activity.name)

    def user_name(self, obj):
        return obj.user.get_profile() and obj.user.get_profile().screen_name or user.username

admin.site.register(AnswerMultiChoice, AnswerMultiChoiceAdmin)
