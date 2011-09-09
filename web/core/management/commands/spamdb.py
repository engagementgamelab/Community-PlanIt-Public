import logging
import random
from optparse import make_option
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from nani.models import TranslatableModel

from django.db import transaction
from django.db.models import get_model
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.localflavor.us.us_states import US_STATES
from django.conf import settings

from core.spammer import random_words, random_email
from instances.models import *
from accounts.models import UserProfile
from values.models import Value, PlayerValue
from missions.models import Mission
from player_activities.models import *
from answers.models import AnswerMultiChoice, AnswerSingleResponse

log = logging.getLogger(__name__)

NOW =  datetime.now()
TODAY = date.today()


cpi_models = [('instances', 'Instance'),
              ('values', 'Value'),
              ('values','PlayerValue'),
              ('missions','Mission'),
              ('player_activities', 'PlayerActivity'),
              ('player_activities', 'PlayerMapActivity'),
              ('player_activities', 'PlayerEmpathyActivity'),
              ('player_activities', 'MultiChoiceActivity'),
              ('auth','User'),
              ('accounts','UserProfile'),
]

def create_admin(instance):
	user = create_user(instance)
	user.is_superuser = True
	user.is_staff = True
	user.username = "admin"
	user.first_name = "Admin"
	user.last_name = "Admin"
	user.email = "admin@cpi.org"
	user.set_password("admin!cpi")
	return user

def create_user(instance):
    kwargs = dict(
            username=random_words(num=1),
            first_name=random_words(num=1), 
            last_name=random_words(num=1), 
            email=random_email(), 
            is_active=True
    )
    u = User.objects.create(**kwargs)
    u.set_password('letmein')
    u.save()
    #user_prof = UserProfile(user=u)
    user_prof = u.get_profile()
    if instance:
    	user_prof.instance = instance
    else:
        user_prof.instance = random.choice(Instance.objects.untranslated())
    user_prof.preferred_language = random.choice(user_prof.instance.languages.all()).code
    user_prof.email = "admin@cpi.org"
    user_prof.save()
    print "UserProfile: %s" % user_prof
    print "User: %s" % u
    return u

def create_instance():

    kwargs = dict(
            start_date=datetime.now(),
            title = random_words(),
            city = random_words(num=2),
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
        inst.description = random_words(l, paragraph=True)[:250]
        inst.save()

    print vars(inst)
    for t in inst.translations.all(): print vars(t)
    inst.save()
    print "Instance: %s" % inst.title
    return inst

def create_value(instance):
    kwargs = dict(
            instance=instance,
    )
    value = Value.objects.create(**kwargs)
    for l in instance.languages.values_list('code', flat=True):
        value.translate(l)
        value.message = random_words(l, paragraph=True)[:10]
        value.save()

    print "Value: %s" % value.pk
    return value

#def create_playervalue(value, user):
#    kwargs = dict(
#            value=value,
#            user=user,
#            coins=random.randint(1, 100),
#    )
#    player_value = PlayerValue.objects.create(**kwargs)
#    print "PlayerValue: %s" % player_value.pk

def create_mission(instance):

    #start_date = TODAY+relativedelta(days=+random.randint(1,90))
    #end_date = start_date+relativedelta(days=+random.randint(1,90))

    kwargs = dict(
            instance=instance,
            title = random_words()[:255],
            video='',
    )
    mission = Mission.objects.create(**kwargs)
    print "Mission: %s" % mission.title

    for l in instance.languages.values_list('code', flat=True):
        mission.translate(l)
        mission.name = random_words(l)[:20]
        mission.description = random_words(l, paragraph=True)[:45]
        mission.save()

    return mission

def create_single_response_activity(activity, instance):
    multichoice_activity = MultiChoiceActivity.objects.create(activity=activity)
    print "MultiChoiceActivity: %s" % multichoice_activity.pk

    for l in instance.languages.values_list('code', flat=True):
        trans = multichoice_activity.translate(l)
        trans.value = random_words(l)[:255]
        multichoice_activity.save()

    #answer_single = AnswerSingleResponse.objects.create(
    #        activity = activity,
    #        answerUser = random.choice(instance.user_profiles.all()).user,
    #        selected = multichoice_activity,
    #)
    print "AnswerSingleResponse: %s" % answer_single.pk

def create_multi_response_activity(activity, instance):
    multichoice_activity = MultiChoiceActivity.objects.create(
            activity=activity,
            )
    print "MultiChoiceActivity: %s" % multichoice_activity.pk
    for l in instance.languages.values_list('code', flat=True):
        trans = multichoice_activity.translate(l)
        trans.value = random_words(l)[:255]
        multichoice_activity.save()

    #answer_multi = AnswerMultiChoice.objects.create(
    #        user = random.choice(instance.user_profiles.all()).user,
    #        option = multichoice_activity,
    #)
    print "AnswerMultiResponse: %s" % answer_multi.pk

def create_activities(mission, instance):
    #map = PlayerActivityType.objects.get(type='map')
    #open_ended = PlayerActivityType.objects.get(type='open_ended')
	#activity_types = (single_res, multi_res, map, open_ended,)

    def create_player_activity(type):
        kwargs = dict(
                creationUser = random.choice(instance.curators.all()),
                mission = mission,
                points = random.randint(1, 100),
                type=type,
        )
        activity = PlayerActivity.objects.create(**kwargs)
        for l in instance.languages.values_list('code', flat=True):
            trans = activity.translate(l)
            trans.name = random_words(l)[:50]
            trans.question = random_words(l, paragraph=True)[:50]
            trans.instructions = random_words(l)[:255]
            trans.addInstructions = random_words(l)[:255]
            activity.save()
        return activity

    multi_res_type = PlayerActivityType.objects.get(type='multi_response')
    multi_res_activity = create_player_activity(type=multi_res_type)
    for x in range(10):
        create_multi_response_activity(multi_res_activity, instance)
        print "MultiResponse PlayerActivity: %s" % activity.pk
        multi_res_activity.save()

    single_res_type = PlayerActivityType.objects.get(type='single_response')
    single_res_activity = create_player_activity(type=single_res_type)
    print "Single Response PlayerActivity: %s" % activity.pk
    for x in range(random.randomint(3,5)):
        create_single_response_activity(multi_res_activity, instance)
        activity.save()

class Command(BaseCommand):
    help = "spam cpi db with new instances and things."

    option_list = BaseCommand.option_list + (
            make_option('--cycles',
                action='store',
                dest='cycles',
                default=1,
                help='number of time to run',
            ),
            make_option('--reset',
                action='store_true',
                dest='reset',
                default=False,
                help='reset all models',
            ),
            make_option('--users-only',
                action='store_true',
                dest='users-only',
                default=False,
                help='create users and exit',
            ),
    )
    #@transaction.commit_manually
    def handle(self, *args, **options):

        try:
            for i in range(0, int(options['cycles'])):
                if options['users-only']:
                    create_user()
                    return
                if options['reset']:
                    for m in cpi_models:
                        cpi_model = get_model(*m)
                        print "deleting %s" % cpi_model
                        if issubclass(cpi_model, TranslatableModel):
                            cpi_model.objects.untranslated().delete()
                        else:
                            cpi_model.objects.all().delete()
                    #transaction.commit()
                #else:
                #    instance = Instance.objects.untranslated()[0]

                for i in range(1):
                    instance = create_instance()
                    if options['reset']:
                        create_admin(instance)
                    for j in range(10):
                        create_user(instance)

                    instance.curators.add(random.choice(UserProfile.objects.filter(instance=instance)).user)
                    instance.save()

                    for j in range(5):
                        mission = create_mission(instance)
                        #create_activities(mission, instance)

                        value = create_value(instance)
                        #for user in User.objects.filter(is_superuser=False):
                        #    for k in range(5):
                        #        create_playervalue(value, user)
                    print "****INSTANCE %s ****" % i

                #transaction.commit()
        except Exception, e:
            log.critical("%s" % e)
            #transaction.rollback()
            raise


