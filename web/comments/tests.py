import unittest, datetime
from django.test import TestCase
from django.contrib.auth.models import User, Group
from web.comments.models import Comment
from web.instances.models import Instance
from django.test.client import Client

class CommentTestCases(TestCase):
    def setUp(self):
        self.email = "testEmail@localhost.com"
        self.instanceName = "Test Instance"
        self.challengeName = "Test Challenge"
        self.c = Client()
        self.instanceStart = datetime.datetime.now()
        self.instanceEnd = datetime.datetime.now() + datetime.timedelta(days=30)
        self.BostonMap = '{"frozen": null, "zoom": 6, "markers": null, "coordinates": [42.355241376822725, -71.060101562500165], "size": [500, 400]}'
        self.LowelMap =  '{"frozen": null, "zoom": 14, "markers": null, "coordinates": [42.638374348203442, -71.315791183471845], "size": [500, 400]}'
        

    def test_create(self):
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": self.email})
        #status_code 302 denotes a redirect but that the same URI should still be used
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        user = User.objects.filter(email=self.email)
        self.assertTrue(len(user) > 0, "The user was created successfully")
        user = user[0]
        
        instance = Instance(name = self.instanceName, 
                            start_date = self.instanceStart,
                            end_date = self.instanceEnd,
                            location = self.BostonMap,
                            curator = user)
        instance.save()

        c = Comment(message = "Test Comment", posted_date=datetime.datetime.now(),
                    flagged=0, user=user, instance=instance)
        c.save()
        c = Comment.objects.filter(message = "Test Comment")
        self.assertTrue(len(c) == 1, "Comment created successfully")
        
class CommentWebTestCases(TestCase):
    def setUp(self):
        self.email1 = "root@localhost.com"
        self.email2 = "testEmail@localhost.com"
        self.instanceName = "Test Instance"
        self.challengeName = "Test Challenge"
        self.c = Client()
        self.instanceStart = datetime.datetime.now()
        self.instanceEnd = datetime.datetime.now() + datetime.timedelta(days=30)
        self.BostonMap = '{"frozen": null, "zoom": 6, "markers": null, "coordinates": [42.355241376822725, -71.060101562500165], "size": [500, 400]}'
        self.LowelMap =  '{"frozen": null, "zoom": 14, "markers": null, "coordinates": [42.638374348203442, -71.315791183471845], "size": [500, 400]}'
        
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": self.email1})
        #status_code 302 denotes a redirect but that the same URI should still be used
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        user = User.objects.filter(email=self.email1)
        self.assertTrue(len(user) > 0, "The user was created successfully")
        self.user1 = user[0]
        
        self.instance = Instance(name = self.instanceName, 
                            start_date = self.instanceStart,
                            end_date = self.instanceEnd,
                            location = self.BostonMap,
                            curator = self.user1)
        self.instance.save()
        
        com1 = Comment(message = "Test Comment", posted_date=datetime.datetime.now(),
                    flagged=0, user=self.user1, instance=self.instance)
        com1.save()
        com1 = Comment.objects.filter(message = "Test Comment")
        self.assertTrue(len(com1) == 1, "Comment created successfully")
        self.com1 = com1[0]
        
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": self.email2, "instance": self.instance.id})
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        user = User.objects.filter(email=self.email2)
        self.assertTrue(len(user) > 0, "The user was created successfully")
        self.user2 = user[0]
        
    def test_like(self):
        response = self.c.post("/comment/like/%d/" % self.com1.id, {"user": self.user2}, HTTP_REFERER="/")
        self.assertTrue(response.status_code == 302, "Reponse is correct")
        com = Comment.objects.get(id=self.com1.id)
        self.assertTrue(com.likes.all().count() == 1, "1 person likes the comment")
    
    def test_flag(self):
        response = self.c.post("/comment/flag/%d/" % self.com1.id, {"user": self.user2}, HTTP_REFERER="/")
        self.assertTrue(response.status_code == 302, "Reponse is correct")
        
        com = Comment.objects.get(id=self.com1.id)
        self.assertTrue(com.flagged == 1, "The comment is now flagged")
    
    def test_reply(self):
        response = self.c.post("/comment/reply/%d/" % self.com1.id, {"user": self.user2, "message": "Response"}, HTTP_REFERER="/")
        self.assertTrue(response.status_code == 302, "Reponse is correct")
        com = Comment.objects.filter(user=self.user2)
        
        self.assertTrue(len(com) == 1, "User2 created a comment")
        
        com = Comment.objects.get(id=self.com1.id)
        self.assertTrue(com.comments.all().count() == 1,"The reply was successfull")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        