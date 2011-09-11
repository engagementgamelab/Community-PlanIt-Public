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

from answers.models import *
admin.site.register(Answer)
admin.site.register(AnswerEmpathy)
admin.site.register(AnswerSingleResponse)
admin.site.register(AnswerMap)
admin.site.register(AnswerMultiChoice)
