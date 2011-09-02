import random
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.localflavor.us.us_states import US_STATES
from django.conf import settings

from core.spammer import random_words

from instances.models import *
from values.models import Value
from missions.models import Mission
#from player_activities.models import *

def create_instance():
    kwargs = dict(
            start_date=datetime.now(),
            title = random_words().decode('iso-8859-1').encode('utf-8'),
            city = random_words(num=2).decode('iso-8859-1').encode('utf-8'),
            state = random.choice(dict(US_STATES).keys()),
    )
    inst = Instance.objects.create(**kwargs)
    for l in dict(settings.LANGUAGES).keys():
        try:
            inst.languages.add(Language.objects.get(code=l))
        except Language.DoesNotExist:
            pass

    for l in inst.languages.values_list('code', flat=True):
        inst.translate(l)
        inst.name = random_words(l).decode('iso-8859-1').encode('utf-8')[:45]
        inst.description = random_words(l, paragraph=True).decode('iso-8859-1').encode('utf-8')[:250]
        inst.save()

    inst.save()
    return inst

def create_value(instance):
    kwargs = dict(
            coins=random.randint(1, 100),
            instance=instance,
    )
    value = Value.objects.create(**kwargs)
    for l in instance.languages.values_list('code', flat=True):
        value.translate(l)
        value.message = random_words(l, paragraph=True).decode('iso-8859-1').encode('utf-8')[:250]
        value.save()
    return value

class Command(BaseCommand):
    help = "spam cpi db with new instances and thigs."

    def handle(self, *args, **options):
        users = User.objects.filter(is_active=True)

        inst = create_instance()

        #for i in range(5):
        #    create_mission(inst)

        for i in range(5):
            create_value(inst)


