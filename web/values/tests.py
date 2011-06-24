import unittest, datetime
from django.test import TestCase
from django.contrib.auth.models import User, Group
from web.accounts.models import UserProfile
from django.test.client import Client
from web.instances.models import Instance
from web.values.models import Value, PlayerValue
from web.comments.models import Comment

class ValuesTestCase(TestCase):
    def setUp(self):
        c = Client()
        email = "test@localhost.com"
        
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
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
        
        comment = Comment()
        comment.message = "This is a new comment message"
        comment.flagged = 0
        comment.hidden = False;
        comment.user = self.user
        comment.instance = self.instance
        comment.save()
        self.assertTrue(Comment.objects.all().count() == 1, "Comment is created")
        self.comment = Comment.objects.all()[0]
    
    def test_create(self):
        value = Value()
        value.message = "This is a message"
        value.coins = 0
        value.instance = self.instance
        value.save()
        self.assertTrue(Value.objects.all().count() == 1, "Value created successfully")
        
    def test_createCoin(self):
        value = Value()
        value.message = "This is a message"
        value.coins = 10
        value.instance = self.instance
        value.save()
        self.assertTrue(Value.objects.all().count() == 1, "Value created successfully")
        value = Value.objects.all()[0]
        self.assertTrue(value.coins == 10, "The coins are correct")
        self.assertTrue(value.message == "This is a message", "Message is correct")
        
    def test_createComment(self):
        value = Value()
        value.message = "This is a message"
        value.coins = 0
        value.instance = self.instance
        #TODO: This should not be like this, fix it.
        value.save()
        
        value = Value.objects.all()[0]
        value.comments = [self.comment]
        value.save()
        self.assertTrue(Value.objects.all().count() == 1, "Value is created successfully")
        value = Value.objects.all()[0]
        self.assertTrue(value.comments != None, "The comment section is not blank")

class ValuesWebTestCase(TestCase):
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
        
        comment = Comment()
        comment.message = "This is a new comment message"
        comment.flagged = 0
        comment.hidden = False;
        comment.user = self.user
        comment.instance = self.instance
        comment.save()
        self.assertTrue(Comment.objects.all().count() == 1, "Comment is created")
        self.comment = Comment.objects.all()[0]
        
        value = Value()
        value.message = "This is a message"
        value.coins = 0
        value.instance = self.instance
        value.comment = self.comment
        value.save()
        self.assertTrue(Value.objects.all().count() == 1, "Value is created successfully")
        self.value = Value.objects.all()[0]
    
    def test_index(self):
        response = self.c.get("/value/")
        self.assertTrue(response.status_code == 200, "/value/ exists and works")
    
    def test_detail(self):
        response = self.c.get("/value/%s/" % self.value.id)
        self.assertTrue(response.status_code == 200, "/value/%s/ exists and works" % self.value.id)
    
    def test_takeFail(self):
        pi = PlayerValue()
        pi.user = self.user
        pi.value = self.value
        pi.coins = 0
        pi.save()
        
        response = self.c.get("/value/take/%s/" % self.value.id, {"user": self.user})
        self.assertTrue(response.status_code == 302, "The coin was taken away, and redirected.")
        
        pi = PlayerValue.objects.filter(value=self.value, user=self.user)
        self.assertTrue(len(pi) == 1, "Player Value retreaved successfully")
        self.assertTrue(pi[0].coins == 0, "The Player Value correctly has 0 coins")
        
        up = UserProfile.objects.get(user = self.user)
        self.assertTrue(up.currentCoins == 0, "UserProfile has correct number of coins")
    
    def test_takeSuccess(self):
        pi = PlayerValue()
        pi.user = self.user
        pi.value = self.value
        pi.coins = 1
        pi.save()
        
        response = self.c.get("/value/take/%s/" % self.value.id, {"user": self.user})
        self.assertTrue(response.status_code == 302, "The coin was taken away, and redirected.")
        
        pi = PlayerValue.objects.filter(value=self.value, user=self.user)
        self.assertTrue(len(pi) == 1, "Player Value retreaved successfully")
        self.assertTrue(pi[0].coins == 0, "The Player Value correctly has 0 coins")
        
        up = UserProfile.objects.get(user = self.user)
        self.assertTrue(up.currentCoins == 1, "UserProfile has correct number of coins")
    
    def test_spendFail(self):
        pi = PlayerValue()
        pi.user = self.user
        pi.value = self.value
        pi.coins = 0
        pi.save()
        
        response = self.c.get("/value/spend/%s/" % self.value.id, {"user": self.user})
        self.assertTrue(response.status_code == 302, "The coin was taken away, and redirected.")
        
        pi = PlayerValue.objects.filter(value=self.value, user=self.user)
        self.assertTrue(len(pi) == 1, "Player Value retreaved successfully")
        self.assertTrue(pi[0].coins == 0, "The Player Value correctly has 0 coins")
        
        up = UserProfile.objects.get(user = self.user)
        self.assertTrue(up.coins == 0, "UserProfile has correct number of coins")
    
    def test_spendFail(self):
        pi = PlayerValue()
        pi.user = self.user
        pi.value = self.value
        pi.coins = 0
        pi.save()
        up = UserProfile.objects.get(user = self.user)
        up.currentCoins = 1
        up.save()
        
        response = self.c.get("/value/spend/%s/" % self.value.id, {"user": self.user})
        self.assertTrue(response.status_code == 302, "The coin was taken away, and redirected.")
        pi = PlayerValue.objects.filter(value=self.value, user=self.user)
        self.assertTrue(len(pi) == 1, "Player Value retreaved successfully")
        self.assertTrue(pi[0].coins == 1, "The Player Value correctly has 1 coin")
        up = UserProfile.objects.get(user = self.user)
        self.assertTrue(up.currentCoins == 0, "UserProfile has correct number of coins")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    