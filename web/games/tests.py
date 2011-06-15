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
from django.contrib.contenttypes.models import ContentType

def createGame(game):
    game.title = "test %s" % game._meta.app_label
    game.content_type = ContentType.objects.get(app_label=game._meta.app_label, name=game._meta.verbose_name)
    game.object_id=1
    game.save()
    return game

class GamesTestCases(TestCase):
    
        
    def test_createMapit(self):
        createGame(Mapit())
        self.assertTrue(Game.objects.all().count() == 1, "Mapit created successfully")
        self.assertTrue(Mapit.objects.all().count() == 1, "Mapit created successfully")
        game = Game.objects.all()[0]
        self.assertTrue(game.game_type == "mapit")

    def test_createThinkfast(self):
        createGame(ThinkFast())
        self.assertTrue(Game.objects.all().count() == 1, "ThinkFast created successfully")
        self.assertTrue(ThinkFast.objects.all().count() == 1, "ThinkFast created successfully")
        game = Game.objects.all()[0]
        self.assertTrue(game.game_type == "thinkfast")
        
    def test_createOthershoes(self):
        createGame(OtherShoes())
        self.assertTrue(Game.objects.all().count() == 1, "OtherShoes created successfully")
        self.assertTrue(OtherShoes.objects.all().count() == 1, "OtherShoes created successfully")
        game = Game.objects.all()[0]
        self.assertTrue(game.game_type == "othershoes")
    
    def test_allThree(self):
        createGame(Mapit())
        createGame(ThinkFast())
        createGame(OtherShoes())
        self.assertTrue(Game.objects.all().count() == 3, "All 3 are created successfully")
   
class GamesWebTestCases(TestCase):
    
    def setUp(self):
        self.mapit = createGame(Mapit())
        self.thinkfast = createGame(ThinkFast())
        self.othershoes = createGame(OtherShoes())
        
        email = "testGame@localhost.com"
        self.c = Client()
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": email})
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        self.user = User.objects.get(email=email)
        
    
    def test_Index(self):
        f = open("/home/ben/djangoOut", "w")
        response = self.c.get("/game/mapit/%s/" % self.mapit.id)
        f.write("%s %s\n" % (response.status_code, response.content))
        self.assertTrue(response.status_code == 200, "mapit url works")
        response = self.c.get("games/thinkfast/%s/" % self.mapit.id)
        self.assertTrue(response.status_code == 200, "mapit url works")
        f.close()
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    