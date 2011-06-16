import unittest, datetime
from django.test import TestCase
from django.contrib.auth.models import User, Group
from web.accounts.models import UserProfile
from django.test.client import Client
from web.instances.models import Instance

class InstanceTestCase(TestCase):
    def test_create(self):
        c = Client()
        email = "testInstance@localhost.com"
        
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": email})
        #status_code 302 denotes a redirect but that the same URI should still be used
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        user = User.objects.filter(email=email)
        self.assertTrue(len(user) > 0, "The user was created successfully")
        user = user[0]
        
        instance = Instance(region="Boston", 
                            start_date=datetime.datetime.now(),
                            end_date=datetime.datetime.now() + datetime.timedelta(days=30),
                            location='{"frozen": null, "zoom": 6, "markers": null, "coordinates": [42.355241376822725, -71.060101562500165], "size": [500, 400]}',
                            curator=user)
        instance.save()
        self.assertTrue(Instance.objects.all().count() == 1, "The instance was created.")
        
class InstanceWebTestCase(TestCase):
    def setUp(self):
        email = "testGame@localhost.com"
        self.c = Client()
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": email})
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        self.user = User.objects.get(email=email)
        
        instance = Instance(region="Boston", 
                            start_date=datetime.datetime.now(),
                            end_date=datetime.datetime.now() + datetime.timedelta(days=30),
                            location='{"frozen": null, "zoom": 6, "markers": null, "coordinates": [42.355241376822725, -71.060101562500165], "size": [500, 400]}',
                            curator=self.user)
        instance.save()
    
    def test_index(self):
        response = self.c.get("/neighborhood/")
        self.assertTrue(response.status_code == 200, "Instance index works")
    
    def test_region(self):
        i = Instance.objects.all()[0]
        response = self.c.get("/neighborhood/%s/" % i.slug)
        self.assertTrue(response.status_code == 200, "Instance region works")
        
                            
                            