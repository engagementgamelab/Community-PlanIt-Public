import unittest, datetime
from django.test import TestCase
from django.contrib.auth.models import User, Group
from web.attachments.models import Attachment
from web.instances.models import Instance
from django.test.client import Client

class AttachmentsTestCases(TestCase):
    def setUp(self):
        self.email = "testEmail@localhost.com"
        self.instanceName = "Test Instance"
        self.challengeName = "Test Challenge"
        self.c = Client()
        self.instanceStart = datetime.datetime.now()
        self.instanceEnd = datetime.datetime.now() + datetime.timedelta(days=30)
        self.BostonMap = '{"frozen": null, "zoom": 6, "markers": null, "coordinates": [42.355241376822725, -71.060101562500165], "size": [500, 400]}'
        self.LowelMap =  '{"frozen": null, "zoom": 14, "markers": null, "coordinates": [42.638374348203442, -71.315791183471845], "size": [500, 400]}'
        self.uploadFile = "/home/ben/Desktop/Viconia.jpg"
    
    #TODO: This doesn't really test file upload, that would require a POST with a FILE field.
    #This only tests that the Attachment can be created. 
    def test_create(self):
        response = self.c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": self.email})
        #status_code 302 denotes a redirect but that the same URI should still be used
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        user = User.objects.filter(email=self.email)
        self.assertTrue(len(user) > 0, "The user was created successfully")
        user = user[0]
        
        att = Attachment(file = self.uploadFile,
                         flagged = 0,
                         user = user)
        att.save()
        att = Attachment.objects.filter(user=user)
        self.assertTrue(len(att) == 1, "Attachment ")
        att = att[0] 
        f = open("/home/ben/djangoOut", "w")
        f.write("attachment file: %s" % att.file)
        f.close()