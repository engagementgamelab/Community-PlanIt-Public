import random
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.localflavor.us.us_states import US_STATES
from django.conf import settings

from core.spammer import random_words
from instances.models import *
from values.models import Value
from missions.models import Mission
#from player_activities.models import *

NOW =  datetime.now()
TODAY = date.today()

def create_instance():


    kwargs = dict(
            start_date=datetime.now(),
            title = random_words(),
            city = random_words(num=2),
            state = random.choice(dict(US_STATES).keys()),
    )
    inst = Instance.objects.create(**kwargs)

    users = User.objects.filter(is_active=True)
    cnum = random.randint(1, users.count()-1)
    curators = [users[i] for i in range(0, cnum)]
    for c in curators:
        inst.currators.add(c)

    for l in dict(settings.LANGUAGES).keys():
        try:
            inst.languages.add(Language.objects.get(code=l))
        except Language.DoesNotExist:
            pass

    for l in inst.languages.values_list('code', flat=True):
        inst.translate(l)
        inst.name = random_words(l)[:45]
        inst.description = random_words(l, paragraph=True)[:250]
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
        value.message = random_words(l, paragraph=True)[:250]
        value.save()
    return value

def create_mission(instance):

    start_date = TODAY+relativedelta(days=+randint(1,90))
    end_date = start_date+relativedelta(days=+randint(1,90))

    kwargs = dict(
            start_date=start_date,
            end_date=end_date,
            instance=instance,
    )
    m = Mission.objects.create(**kwargs)
    for l in instance.languages.values_list('code', flat=True):
        m.translate(l)
        m.name = random_words(l, paragraph=True)[:45]
        m.description = random_words(l, paragraph=True)[:45]
        m.save()
    return m

class Command(BaseCommand):
    help = "spam cpi db with new instances and things."

    option_list = BaseCommand.option_list + (
            make_option('--cycles',
                action='store',
                dest='cycles',
                default=1,
                help='number of time to run',
            ),
    )
    @transaction.commit_manually
    def handle(self, *args, **options):
        for i in options['cycles']:

            inst = create_instance()

            for i in range(5):
                create_mission(inst)
                create_value(inst)
            transaction.commit()


