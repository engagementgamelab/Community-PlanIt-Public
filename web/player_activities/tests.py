from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from core.test_fixtures import create_fixtures
from player_activities.models import PlayerActivity, PlayerActivityType,\
    MultiChoiceActivity, PlayerMapActivity
from missions.models import Mission
from web.comments.forms import CommentForm
from answers.models import Answer


class OpenEndedActivityTest(TestCase):
    def setUp(self):
        create_fixtures()
        self.client = Client()                   
        self.assertTrue(self.client.login(username="admin", password="admin"))
        
        self.user = User.objects.get(username="admin")
        mission = Mission.objects.untranslated().get(pk=1)
        activity_type=PlayerActivityType.objects.get(type="open_ended")

        self.open_ended = PlayerActivity.objects.language('en-us').create(creationUser=self.user,
                                                                       mission=mission,
                                                                       type=activity_type)
        
    def test_overview(self):
        response = self.client.get(reverse("activities:player_activities_overview", 
                                           args=[self.open_ended.pk]))
        self.assertEqual(200, response.status_code)
        
    def test_get_activity(self):
        response = self.client.get(reverse("activities:player_activities_activity", 
                                           args=[self.open_ended.pk]))
        
        self.assertFalse(response.context['form'])
        comment_form = response.context['comment_form']
        self.assertFalse(comment_form.just_one_form)
        self.assertTrue(comment_form.allow_replies)
        self.assertEqual(self.open_ended, response.context['activity'])
        self.assertFalse(response.context['map'])
        self.assertFalse(response.context['init_coords'])
        
        self.assertEqual(200, response.status_code)
        
    def test_get_activity_post(self):
        answers = Answer.objects.filter(activity=self.open_ended, answerUser=self.user)
        self.assertEqual(0, answers.count())
        
        context = {'form': 'open_ended',
                   'message': 'Hi'}
        response = self.client.post(reverse("activities:player_activities_activity", 
                                           args=[self.open_ended.pk]),
                                    context)
        self.assertEqual(302, response.status_code)
        
        answers = Answer.objects.filter(activity=self.open_ended, answerUser=self.user)
        self.assertEqual(1, answers.count())
        self.assertEqual('Hi', answers[0].comments.language('en').message)
        
    def test_get_activity_with_answers(self):
        Answer.objects.create(activity=self.open_ended, answerUser=self.user)
        response = self.client.get(reverse("activities:player_activities_activity", 
                                           args=[self.open_ended.pk]))
        self.assertRedirects(response, reverse("activities:player_activities_replay", 
                                           args=[self.open_ended.pk]),
                             target_status_code=404)
    #TODO: add comments, test overview with comments and answers
    
    def test_replay_is_not_allowed(self):        
        response = self.client.get(reverse("activities:player_activities_replay", 
                                           args=[self.open_ended.pk]))
        self.assertEqual(404, response.status_code)        
        

class SingleResponseActivityTest(TestCase):
    def setUp(self):
        create_fixtures()
        self.client = Client()                   
        self.assertTrue(self.client.login(username="admin", password="admin"))
        
        user = User.objects.get(username="admin")
        mission = Mission.objects.untranslated().get(pk=1)
        activity_type=PlayerActivityType.objects.get(type="single_response")
        self.single_response = PlayerActivity.objects.language('en-us').create(creationUser=user,
                                                                            mission=mission,
                                                                            type=activity_type)
        
    def test_overview(self):
        response = self.client.get(reverse("activities:player_activities_overview", 
                                           args=[self.single_response.pk]))
        self.assertEqual(200, response.status_code)
        
    def test_get_activity(self):
        response = self.client.get(reverse("activities:player_activities_activity", 
                                           args=[self.single_response.pk]))
        self.assertEqual(200, response.status_code)
        
    #TODO: add comments, test overview with comments and answers
        
    def test_replay_is_allowed(self):        
        response = self.client.get(reverse("activities:player_activities_replay", 
                                           args=[self.single_response.pk]))
        self.assertEqual(200, response.status_code)
        
    def test_post_replay(self):
        choice = MultiChoiceActivity.objects.language('en-us').create(activity=self.single_response, 
                                                            value="test value")
        context = {'form': 'single_response',
                   'response': choice.pk}
        response = self.client.post(reverse("activities:player_activities_replay", 
                                           args=[self.single_response.pk]), context)
        
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://testserver/en/activities/%s/overview/' % self.single_response.pk,
                         response.get('location', ''))
        #TODO: check that answers were created


class MultiResponsesActivityTest(TestCase):
    def setUp(self):
        create_fixtures()
        self.client = Client()                   
        self.assertTrue(self.client.login(username="admin", password="admin"))
        
        user = User.objects.get(username="admin")
        mission = Mission.objects.untranslated().get(pk=1)
        activity_type=PlayerActivityType.objects.get(type="multi_response")
        self.multi_responses = PlayerActivity.objects.language('en-us').create(creationUser=user,
                                                                            mission=mission,
                                                                            type=activity_type)
        
    def test_overview(self):
        response = self.client.get(reverse("activities:player_activities_overview", 
                                           args=[self.multi_responses.pk]))
        self.assertEqual(200, response.status_code)
    
    def test_get_activity(self):
        response = self.client.get(reverse("activities:player_activities_activity", 
                                           args=[self.multi_responses.pk]))
        self.assertEqual(200, response.status_code)
        
    #TODO: add comments, test overview with comments and answers
        
    def test_replay_is_allowed(self):        
        response = self.client.get(reverse("activities:player_activities_replay", 
                                           args=[self.multi_responses.pk]))
        self.assertEqual(200, response.status_code)
        
    def test_post_replay(self):
        choice = MultiChoiceActivity.objects.language('en-us').create(activity=self.multi_responses, 
                                                            value="test value")
        context = {'form': 'multi_response',
                   'response_1': [choice.pk,]}
        response = self.client.post(reverse("activities:player_activities_replay", 
                                           args=[self.multi_responses.pk]), context)
        
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://testserver/en/activities/%s/overview/' % self.multi_responses.pk,
                         response.get('location', ''))
        #TODO: check that answers were created


class MapActivityTest(TestCase):
    def setUp(self):
        create_fixtures()
        self.client = Client()                   
        self.assertTrue(self.client.login(username="admin", password="admin"))
        
        user = User.objects.get(username="admin")
        mission = Mission.objects.untranslated().get(pk=1)
        activity_type=PlayerActivityType.objects.get(type="map")
        self.map = PlayerActivity.objects.language('en-us').create(creationUser=user,
                                                                mission=mission,
                                                                type=activity_type)
        # Attention: to make the tests pass we need both PlayerActivity and PlayerMapActivity
        # Is this correct?
        PlayerMapActivity.objects.language('en-us').create(creationUser=user,
                                                        mission=mission,
                                                        type=activity_type)
        
        
    def test_overview(self):
        response = self.client.get(reverse("activities:player_activities_overview", 
                                           args=[self.map.pk]))
        self.assertEqual(200, response.status_code)
    
    def test_get_activity(self):
        response = self.client.get(reverse("activities:player_activities_activity", 
                                           args=[self.map.pk]))
        self.assertEqual(200, response.status_code)
        
    #TODO: add comments, test overview with comments and answers
        
    def test_replay_is_allowed(self):        
        response = self.client.get(reverse("activities:player_activities_replay", 
                                           args=[self.map.pk]))
        self.assertEqual(200, response.status_code)
        
    def test_post_replay(self):
        context = {'form': 'map',
                   'map': '{"coordinates":[40.71435281518603,-74.0059731],"zoom":10,"markers":[{"coordinates":[40.7143528,-74.0059731]}],"type":"Point"}',
                  }
        response = self.client.post(reverse("activities:player_activities_replay", 
                                           args=[self.map.pk]), context)
        
        self.assertEqual(302, response.status_code)
        self.assertEqual('http://testserver/en/activities/%s/overview/' % self.map.pk,
                         response.get('location', ''))
        #TODO: check that answers were created
        

class EmpathyActivityTest(TestCase):
    def setUp(self):
        create_fixtures()
        self.client = Client()                   
        self.assertTrue(self.client.login(username="admin", password="admin"))
        
        user = User.objects.get(username="admin")
        mission = Mission.objects.untranslated().get(pk=1)
        activity_type=PlayerActivityType.objects.get(type="empathy")
        self.empaty = PlayerActivity.objects.language('en-us').create(creationUser=user,
                                                                mission=mission,
                                                                type=activity_type)       
        
    def test_overview(self):
        response = self.client.get(reverse("activities:player_activities_overview", 
                                           args=[self.empaty.pk]))
        self.assertEqual(200, response.status_code)
        
    def test_get_activity(self):
        response = self.client.get(reverse("activities:player_activities_activity", 
                                           args=[self.empaty.pk]))
        self.assertEqual(200, response.status_code)
        
    #TODO: add comments, test overview with comments and answers
        
    def test_replay_is_not_allowed(self):        
        response = self.client.get(reverse("activities:player_activities_replay", 
                                           args=[self.empaty.pk]))

        self.assertEqual(404, response.status_code)        
  
