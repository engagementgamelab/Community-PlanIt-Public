import unittest, datetime
from django.test import TestCase
from django.contrib.auth.models import User, Group
from web.accounts.models import UserProfile
from django.test.client import Client
from web.instances.models import Instance
from web.issues.models import Issue, PlayerIssue
from web.comments.models import Comment

class IssuesTestCase(TestCase):
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
        
        instance = Instance(region="Boston", 
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
        issue = Issue()
        issue.message = "This is a message"
        issue.coins = 0
        issue.instance = self.instance
        issue.save()
        self.assertTrue(Issue.objects.all().count() == 1, "Issue created successfully")
        
    def test_createCoin(self):
        issue = Issue()
        issue.message = "This is a message"
        issue.coins = 10
        issue.instance = self.instance
        issue.save()
        self.assertTrue(Issue.objects.all().count() == 1, "Issue created successfully")
        issue = Issue.objects.all()[0]
        self.assertTrue(issue.coins == 10, "The coins are correct")
        self.assertTrue(issue.message == "This is a message", "Message is correct")
        
    def test_createComment(self):
        issue = Issue()
        issue.message = "This is a message"
        issue.coins = 0
        issue.instance = self.instance
        #TODO: This should not be like this, fix it.
        issue.save()
        
        issue = Issue.objects.all()[0]
        issue.comments = [self.comment]
        issue.save()
        self.assertTrue(Issue.objects.all().count() == 1, "Issue is created successfully")
        issue = Issue.objects.all()[0]
        self.assertTrue(issue.comments != None, "The comment section is not blank")

class IssuesWebTestCase(TestCase):
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
        
        instance = Instance(region="Boston", 
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
        
        issue = Issue()
        issue.message = "This is a message"
        issue.coins = 0
        issue.instance = self.instance
        issue.comment = self.comment
        issue.save()
        self.assertTrue(Issue.objects.all().count() == 1, "Issue is created successfully")
        self.issue = Issue.objects.all()[0]
    
    def test_index(self):
        response = self.c.get("/issue/")
        self.assertTrue(response.status_code == 200, "/issue/ exists and works")
    
    def test_detail(self):
        response = self.c.get("/issue/%s/" % self.issue.id)
        self.assertTrue(response.status_code == 200, "/issue/%s/ exists and works" % self.issue.id)
    
    def test_takeFail(self):
        pi = PlayerIssue()
        pi.user = self.user
        pi.issue = self.issue
        pi.coins = 0
        pi.save()
        
        response = self.c.get("/issue/take/%s/" % self.issue.id, {"user": self.user})
        self.assertTrue(response.status_code == 302, "The coin was taken away, and redirected.")
        
        pi = PlayerIssue.objects.filter(issue=self.issue, user=self.user)
        self.assertTrue(len(pi) == 1, "Player Issue retreaved successfully")
        self.assertTrue(pi[0].coins == 0, "The Player Issue correctly has 0 coins")
        
        up = UserProfile.objects.get(user = self.user)
        self.assertTrue(up.coins == 0, "UserProfile has correct number of coins")
    
    def test_takeSuccess(self):
        pi = PlayerIssue()
        pi.user = self.user
        pi.issue = self.issue
        pi.coins = 1
        pi.save()
        
        response = self.c.get("/issue/take/%s/" % self.issue.id, {"user": self.user})
        self.assertTrue(response.status_code == 302, "The coin was taken away, and redirected.")
        
        pi = PlayerIssue.objects.filter(issue=self.issue, user=self.user)
        self.assertTrue(len(pi) == 1, "Player Issue retreaved successfully")
        self.assertTrue(pi[0].coins == 0, "The Player Issue correctly has 0 coins")
        
        up = UserProfile.objects.get(user = self.user)
        self.assertTrue(up.coins == 1, "UserProfile has correct number of coins")
    
    def test_spendFail(self):
        pi = PlayerIssue()
        pi.user = self.user
        pi.issue = self.issue
        pi.coins = 0
        pi.save()
        
        response = self.c.get("/issue/spend/%s/" % self.issue.id, {"user": self.user})
        self.assertTrue(response.status_code == 302, "The coin was taken away, and redirected.")
        
        pi = PlayerIssue.objects.filter(issue=self.issue, user=self.user)
        self.assertTrue(len(pi) == 1, "Player Issue retreaved successfully")
        self.assertTrue(pi[0].coins == 0, "The Player Issue correctly has 0 coins")
        
        up = UserProfile.objects.get(user = self.user)
        self.assertTrue(up.coins == 0, "UserProfile has correct number of coins")
    
    def test_spendFail(self):
        pi = PlayerIssue()
        pi.user = self.user
        pi.issue = self.issue
        pi.coins = 0
        pi.save()
        up = UserProfile.objects.get(user = self.user)
        up.coins = 1
        up.save()
        
        response = self.c.get("/issue/spend/%s/" % self.issue.id, {"user": self.user})
        self.assertTrue(response.status_code == 302, "The coin was taken away, and redirected.")
        
        pi = PlayerIssue.objects.filter(issue=self.issue, user=self.user)
        self.assertTrue(len(pi) == 1, "Player Issue retreaved successfully")
        self.assertTrue(pi[0].coins == 1, "The Player Issue correctly has 0 coins")
        
        up = UserProfile.objects.get(user = self.user)
        self.assertTrue(up.coins == 0, "UserProfile has correct number of coins")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    