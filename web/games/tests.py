import unittest, datetime
from django.test import TestCase
from django.contrib.auth.models import User, Group
from web.attachments.models import Attachment
from web.instances.models import Instance
from django.test.client import Client
from web.games.models import *
from web.games.mapit.models import *
from web.games.othershoes.models import *
from web.games.thinkfast.models import *
from web.missions.models import Mission 
from django.contrib.contenttypes.models import ContentType

def createGame(game, mission):
    game.title = "test %s" % game._meta.app_label
    game.content_type = ContentType.objects.get(app_label=game._meta.app_label, name=game._meta.verbose_name)
    game.object_id=1
    game.mission = mission
    game.save()
    return game

class GamesTestCases(TestCase):
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
        
        mission = Mission()
        mission.topic = "this is a topic"
        mission.start_date = datetime.datetime.now()
        mission.end_date = datetime.datetime.now() + datetime.timedelta(days=30)
        mission.instance = self.instance
        mission.save()
        self.assertTrue(Mission.objects.all().count() == 1, "Mission created successfully")
        self.mission = Mission.objects.all()[0]
        
    def test_createMapit(self):
        createGame(Mapit(), self.mission)
        self.assertTrue(Game.objects.all().count() == 1, "Mapit created successfully")
        self.assertTrue(Mapit.objects.all().count() == 1, "Mapit created successfully")
        game = Game.objects.all()[0]
        self.assertTrue(game.game_type == "mapit")
        self.assertTrue(game.mission != None, "Mission tied to game")

    def test_createThinkfast(self):
        createGame(ThinkFast(), self.mission)
        self.assertTrue(Game.objects.all().count() == 1, "ThinkFast created successfully")
        self.assertTrue(ThinkFast.objects.all().count() == 1, "ThinkFast created successfully")
        game = Game.objects.all()[0]
        self.assertTrue(game.game_type == "thinkfast")
        self.assertTrue(game.mission != None, "Mission tied to game")
        
    def test_createOthershoes(self):
        createGame(OtherShoes(), self.mission)
        self.assertTrue(Game.objects.all().count() == 1, "OtherShoes created successfully")
        self.assertTrue(OtherShoes.objects.all().count() == 1, "OtherShoes created successfully")
        game = Game.objects.all()[0]
        self.assertTrue(game.game_type == "othershoes")
        self.assertTrue(game.mission != None, "Mission tied to game")
    
    def test_allThree(self):
        game = createGame(Mapit(), self.mission)
        self.assertTrue(game.mission != None, "Mission tied to game")
        
        game = createGame(ThinkFast(), self.mission)
        self.assertTrue(game.mission != None, "Mission tied to game")
        
        game = createGame(OtherShoes(), self.mission)
        self.assertTrue(game.mission != None, "Mission tied to game")
        
        self.assertTrue(Game.objects.all().count() == 3, "All 3 are created successfully")
   
class GamesWebTestCases(TestCase):
    
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
        
        up = self.user.get_profile()
        up.instance = self.instance
        up.save()
        
        mission = Mission()
        mission.topic = "this is a topic"
        mission.start_date = datetime.datetime.now()
        mission.end_date = datetime.datetime.now() + datetime.timedelta(days=30)
        mission.instance = self.instance
        mission.save()
        self.assertTrue(Mission.objects.all().count() == 1, "Mission created successfully")
        self.mission = Mission.objects.all()[0]
        
        self.mapit = createGame(Mapit(), self.mission)
        self.assertTrue(self.mapit.mission != None, "mapit has mission")
        
        self.thinkfast = createGame(ThinkFast(), self.mission)
        self.assertTrue(self.thinkfast.mission != None, "thinkfast has mission")
        
        self.othershoes = createGame(OtherShoes(), self.mission)
        self.assertTrue(self.othershoes.mission != None, "othershoes has mission")

        
    
    def test_Index(self):
        response = self.c.get("/game/mapit/%s/" % self.mapit.id, {"user": self.user})
        self.assertTrue(response.status_code == 200, "mapit url works")
        response = self.c.get("/game/thinkfast/%s/" % self.thinkfast.id)
        self.assertTrue(response.status_code == 200, "mapit url works")
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    