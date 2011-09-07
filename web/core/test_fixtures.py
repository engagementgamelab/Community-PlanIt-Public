import datetime

from django.contrib.auth.models import User

from accounts.models import UserProfile
from instances.models import Instance, Language
from missions.models import Mission
from values.models import Value
from player_activities.models import PlayerActivityType


def create_fixtures():
    """
    Create initial data for tests.
    """
    su = User.objects.get_or_create(
            email='admin@admin.com',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            username='admin',
    )[0]
    su.set_password('admin')
    su.save()   
    
    language = Language.objects.create(code='en-us', name='English')
    
    instance = _create_instance(language)
    
    _create_user_profile(su, instance)
    
    _create_mission(instance)
    
    _create_player_activity_types()
    
    Value.objects.create(instance=instance, message="test")


def _create_user_profile(user, instance):
    profile = UserProfile.objects.get_or_create(user=user)[0]
    profile.preferred_language = 'ht'
    profile.instance = instance
    profile.save()    


def _create_instance(language):
    en_instance = Instance.objects.language('en-us').create(
            slug='test',
            title='Test Title',
            city='Los Angeles',
            state='CA',
            start_date='2011-09-05 00:48:40',           
            location='{"coordinates":[0,0],"zoom":16,"markers":[{"coordinates":[0,0]}],"type":"Point"}',
            name='English',
            description='EnglishDesc'
    )     
    en_instance.languages = (language,)
    en_instance.save()  
    
    es_instance = en_instance.translate('es')
    es_instance.name = "Es test"
    es_instance.description = "Es test description"
    es_instance.save()
    
    ht_instance = en_instance.translate('ht')
    ht_instance.name = "Ht test"
    ht_instance.description = "Ht test description"
    ht_instance.save()   
    
    return en_instance 


def _create_mission(instance):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(1)
    yesterday = today - datetime.timedelta(1)
    
    en_mission = Mission.objects.language('en-us').create(instance=instance,
                                                       start_date=yesterday,
                                                       end_date=tomorrow,
                                                       name="mission",
                                                       description="test")
    en_mission.translate('es')
    en_mission.translate('ht')
    return en_mission


def _create_player_activity_types():
    PlayerActivityType.objects.get_or_create(type="open_ended", displayType="Open Ended")
    PlayerActivityType.objects.get_or_create(type="single_response", displayType="Single Response")
    PlayerActivityType.objects.get_or_create(type="multi_response", displayType="Multiple Responses")
    PlayerActivityType.objects.get_or_create(type="map", displayType="Map")
    PlayerActivityType.objects.get_or_create(type="empathy", displayType="Empathy")
    
