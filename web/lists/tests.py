import unittest, datetime
from django.test import TestCase
from django.contrib.auth.models import User, Group
from web.accounts.models import UserProfile
from django.test.client import Client
from web.instances.models import Instance

class ListWebTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        email = "test@localhost.com"
        
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": email})
        #status_code 302 denotes a redirect but that the same URI should still be used
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        user = User.objects.filter(email=email)
        self.assertTrue(len(user) > 0, "The user was created successfully")
        self.user1 = user[0]
        
        instance = Instance(name="Boston", 
                            start_date=datetime.datetime.now(),
                            end_date=datetime.datetime.now() + datetime.timedelta(days=30),
                            location='{"frozen": null, "zoom": 6, "markers": null, "coordinates": [42.355241376822725, -71.060101562500165], "size": [500, 400]}',
                            curator=self.user1)
        instance.save()
        self.assertTrue(Instance.objects.all().count() == 1, "The instance was created.")
        self.instance = Instance.objects.all()[0]
        
        email = "test1@localhost.com"
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": email})
        #status_code 302 denotes a redirect but that the same URI should still be used
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        user = User.objects.filter(email=email)
        self.assertTrue(len(user) > 0, "The user was created successfully")
        self.user2 = user[0]
        
        profile1 = self.user1.get_profile()
        profile2 = self.user2.get_profile()
        
        profile1.following = [self.user2]
        profile1.save()
        
        profile2.following = [self.user1]
        profile2.save()
        
    def test_neighborhood(self):
        response = self.c.get("/list/neighborhood/%s/" % self.instance.slug)
        self.assertTrue(response.status_code == 200, "The neighborhood link is valid")
    
    def test_following(self):
        response = self.c.get("/list/following/%s/" % self.user1.id)
        self.assertTrue(response.status_code == 200, "The following link is valid")
    
    def test_followers(self):
        response = self.c.get("/list/followers/%s/" % self.user1.id)
        self.assertTrue(response.status_code == 200, "The followers link is valid")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        