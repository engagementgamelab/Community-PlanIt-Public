import unittest, datetime
from django.test import TestCase
from django.contrib.auth.models import User, Group
from web.challenges.models import Challenge
from web.instances.models import Instance, InstanceView
from django.test.client import Client

class ChallengesTestCases(TestCase):
    
    #finish this off after instance unit tests
    
    def test_addChallenge(self):
        #This is exactly the same as the accounts test test_login
        email = "addChallenge@localhost.com"
        c = Client()
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": email})
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        
        user = User.objects.filter(email=email)
        self.assertTrue(len(user) == 1, "User created successfully")
        user = user[0]
        
        instance = Instance(name="Test Add Challenge", 
                            start_date=datetime.datetime.now(),
                            end_date=datetime.datetime.now() + datetime.timedelta(days=30),
                            location='{"frozen": null, "zoom": 6, "markers": null, "coordinates": [42.355241376822725, -71.060101562500165], "size": [500, 400]}',
                            curator=user)
        instance.save()
        self.assertTrue(Instance.objects.all().count() == 1, "The instance was created.")
        instance = Instance.objects.get(name="Test Add Challenge")
        challenge = Challenge(map = '{"frozen": null, "zoom": 6, "markers": null, "coordinates": [42.355241376822725, -71.060101562500165], "size": [500, 400]}',
                              name = "Test challenge",
                              description = "Test challenge",
                              start_date = datetime.datetime.now(),
                              end_date = datetime.datetime.now() + datetime.timedelta(days=14),
                              instance = InstanceView.objects.get(id = instance.id),
                              user=user
                              )
        challenge.save()
        chal = Challenge.objects.filter(name = "Test challenge")
        self.assertTrue(len(chal) == 1, "The challenge was created successfully")

class ChallengesWebTestCases(TestCase):        
    
    def setUp(self):
        self.email = "testEmail@localhost.com"
        self.instanceName = "Test Instance"
        self.challengeName = "Test Challenge"
        self.c = Client()
        self.BostonMap = '{"frozen": null, "zoom": 6, "markers": null, "coordinates": [42.355241376822725, -71.060101562500165], "size": [500, 400]}'
        self.LowelMap =  '{"frozen": null, "zoom": 14, "markers": null, "coordinates": [42.638374348203442, -71.315791183471845], "size": [500, 400]}'
        self.instanceStart = datetime.datetime.now()
        self.instanceEnd = datetime.datetime.now() + datetime.timedelta(days=30)
        self.challengeStart = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        self.challengeEnd = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%m/%d/%Y %H:%M:%S")
         
    def test_addChallenge(self):
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                      "lastName": "new_test", "email": "root@localhost.com"})
        self.assertTrue(response.status_code == 302, "User created successfully")
        user = User.objects.filter(email="root@localhost.com")
        self.assertTrue(len(user) == 1, "User created successfully")
        user = user[0]
        
        instance = Instance(name = self.instanceName, 
                            start_date = self.instanceStart,
                            end_date = self.instanceEnd,
                            location = self.BostonMap,
                            curator = user)
        instance.save()
        self.assertTrue(Instance.objects.all().count() == 1, "Instance created successfully")
        instance = Instance.objects.get(name = self.instanceName)
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": self.email, "instance": instance.id})
        fout = open("/home/ben/djangoOut", "w")
        fout.write("Content: %s" % response.content)
        self.assertTrue(response.status_code == 302, "User created successfully")
        
        user = User.objects.filter(email=self.email)
        self.assertTrue(len(user) == 1, "User created successfully")
        user = user[0]
    
        response = self.c.post("/challenge/add/", {"map": self.LowelMap,
                                                   "name": self.challengeName,
                                                   "description": "This is a description",
                                                   "start_date": self.challengeStart,
                                                   "end_date": self.challengeEnd,
                                                   "user": user})
        self.assertTrue(response.status_code == 302, "challenge was POSTed successfully")
        challenge = Challenge.objects.filter(name= self.challengeName)
        self.assertTrue(len(challenge) == 1, "Challenge created successfully")
    
    def test_fetch(self):
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                      "lastName": "new_test", "email": "root@localhost.com"})
        self.assertTrue(response.status_code == 302, "User created successfully")
        user = User.objects.filter(email="root@localhost.com")
        self.assertTrue(len(user) == 1, "User created successfully")
        user = user[0]
        
        instance = Instance(name = self.instanceName, 
                            start_date = self.instanceStart,
                            end_date = self.instanceEnd,
                            location = self.BostonMap,
                            curator = user)
        instance.save()
        self.assertTrue(Instance.objects.all().count() == 1, "Instance created successfully")
        instance = Instance.objects.get(name = self.instanceName)
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": self.email, "instance": instance.id})
        self.assertTrue(response.status_code == 302, "User created successfully")
        
        user = User.objects.filter(email=self.email)
        self.assertTrue(len(user) == 1, "User created successfully")
        user = user[0]
    
        response = self.c.post("/challenge/add/", {"map": self.LowelMap,
                                                   "name": self.challengeName,
                                                   "description": "This is a description",
                                                   "start_date": self.challengeStart,
                                                   "end_date": self.challengeEnd,
                                                   "user": user})
        self.assertTrue(response.status_code == 302, "challenge was POSTed successfully")
        challenge = Challenge.objects.filter(name= self.challengeName)
        self.assertTrue(len(challenge) == 1, "Challenge created successfully")
        challenge = challenge[0]
        
        response = self.c.get("/challenge/%d/" % challenge.id)
        self.assertTrue(response.status_code == 200, "Fetched the challenge correctly")


        
        
        
        
        
        
        