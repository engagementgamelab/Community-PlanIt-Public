import unittest, datetime
from django.test import TestCase
from django.contrib.auth.models import User, Group
from web.accounts.models import UserProfile
from django.test.client import Client
from web.instances.models import Instance
from web.values.models import Value, PlayerValue
from web.comments.models import Comment
from web.missions.models import Mission
from web.games.models import *
from web.games.mapit.models import *

def createGame(game, mission):
    game.title = "test %s" % game._meta.app_label
    game.content_type = ContentType.objects.get(app_label=game._meta.app_label, name=game._meta.verbose_name)
    game.object_id=1
    game.mission = mission
    game.save()
    return game

class MissionsTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        email = "test@localhost.com"
        
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": email})
        #status_code 302 denotes a redirect but that the same URI should still be used
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        user = User.objects.filter(email=email)
        self.assertTrue(len(user) > 0, "The user was created successfully")
        self.user = user[0]
        
        instance = Instance(name="Boston", 
                            start_date=datetime.datetime.now(),
                            end_date=datetime.datetime.now() + datetime.timedelta(days=30),
                            location='{"frozen": null, "zoom": 6, "markers": null, "coordinates": [42.355241376822725, -71.060101562500165], "size": [500, 400]}',
                            curator=self.user)
        instance.save()
        self.assertTrue(Instance.objects.all().count() == 1, "The instance was created.")
        self.instance = Instance.objects.all()[0]
    
    def test_create(self):
        mission = Mission()
        mission.topic = "this is a topic"
        mission.start_date = datetime.datetime.now()
        mission.end_date = datetime.datetime.now() + datetime.timedelta(days=30)
        mission.instance = self.instance
        mission.save()
        self.assertTrue(Mission.objects.all().count() == 1, "Mission created successfully")

class MissionsWebTestCase(TestCase):    
    def setUp(self):
        self.c = Client()
        email = "test@localhost.com"
        
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": email})
        #status_code 302 denotes a redirect but that the same URI should still be used
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        user = User.objects.filter(email=email)
        self.assertTrue(len(user) > 0, "The user was created successfully")
        self.user = user[0]
        
        instance = Instance(name="Boston", 
                            start_date=datetime.datetime.now(),
                            end_date=datetime.datetime.now() + datetime.timedelta(days=30),
                            location='{"frozen": null, "zoom": 6, "markers": null, "coordinates": [42.355241376822725, -71.060101562500165], "size": [500, 400]}',
                            curator=self.user)
        instance.save()
        self.assertTrue(Instance.objects.all().count() == 1, "The instance was created.")
        self.instance = Instance.objects.all()[0]
        
    def test_index(self):
        response = self.c.get("/mission/", {"user": self.user})
        self.assertTrue(response.status_code == 200, "Mission index page works")
    
    def test_fetchFromSlug(self):
        mission = Mission()
        mission.topic = "this is a topic"
        mission.start_date = datetime.datetime.now()
        mission.end_date = datetime.datetime.now() + datetime.timedelta(days=30)
        mission.instance = self.instance
        mission.save()
        self.assertTrue(Mission.objects.all().count() == 1, "Mission created successfully")
        misison = Mission.objects.all()[0]
        
        response = self.c.get("/mission/%s/" % mission.slug, {"user": self.user})
        self.assertTrue(response.status_code == 200, "Mission fetch from slug page works")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    