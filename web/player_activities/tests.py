from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from core.test_fixtures import create_fixtures
from player_activities.models import PlayerActivity, PlayerActivityType,\
    MultiChoiceActivity
from missions.models import Mission
from django.core.urlresolvers import reverse


class OpenEndedActivityTest(TestCase):
    def setUp(self):
        create_fixtures()
        self.client = Client()                   
        self.assertTrue(self.client.login(username="admin", password="admin"))
        
        user = User.objects.get(username="admin")
        mission = Mission.objects.untranslated().get(pk=1)
        activity_type=PlayerActivityType.objects.get(type="open_ended")
        self.open_ended = PlayerActivity.objects.language('en').create(creationUser=user,
                                                                       mission=mission,
                                                                       type=activity_type)
        
    def test_overview(self):
        response = self.client.get(reverse("activities:player_activities_overview", 
                                           args=[self.open_ended.pk]))
        self.assertEqual(200, response.status_code)
        
    #TODO: add comments, test overview with comments and answers
    
    def test_replay_is_not_allowed(self):        
        response = self.client.get(reverse("activities:player_activities_replay", 
                                           args=[self.open_ended.pk]))
        self.assertEqual(404, response.status_code)        
        
    def test_post_replay(self):
        context = {'form': 'open_ended'}
        response = self.client.post(reverse("activities:player_activities_replay", 
                                           args=[self.open_ended.pk]), context)
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://testserver/en/activities/%s/overview/' % self.open_ended.pk,
                         response.get('location', ''))
        

class SingleResponseActivityTest(TestCase):
    def setUp(self):
        create_fixtures()
        self.client = Client()                   
        self.assertTrue(self.client.login(username="admin", password="admin"))
        
        user = User.objects.get(username="admin")
        mission = Mission.objects.untranslated().get(pk=1)
        activity_type=PlayerActivityType.objects.get(type="single_response")
        self.single_response = PlayerActivity.objects.language('en').create(creationUser=user,
                                                                            mission=mission,
                                                                            type=activity_type)
        
    def test_overview(self):
        response = self.client.get(reverse("activities:player_activities_overview", 
                                           args=[self.single_response.pk]))
        self.assertEqual(200, response.status_code)
        
    #TODO: add comments, test overview with comments and answers
        
    def test_replay_is_allowed(self):        
        response = self.client.get(reverse("activities:player_activities_replay", 
                                           args=[self.single_response.pk]))
        self.assertEqual(200, response.status_code)
        
    def test_post_replay(self):
        choice = MultiChoiceActivity.objects.language('en').create(activity=self.single_response, 
                                                            value="test value")
        context = {'form': 'single_response',
                   'response': choice.pk}
        response = self.client.post(reverse("activities:player_activities_replay", 
                                           args=[self.single_response.pk]), context)
        
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://testserver/en/activities/%s/overview/' % self.single_response.pk,
                         response.get('location', ''))
        
    
        