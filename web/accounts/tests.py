import unittest
from django.test import TestCase
from django.contrib.auth.models import User, Group
from web.accounts.models import UserProfile
from django.test.client import Client
from PIL import Image
from settings import MEDIA_ROOT
# For testing Accounts
# TODO: Testing the registration of users with an instance is tested under
# challenges. Creation of an instance via the web and directly using models
# should be placed under instances. Eventually when instances can be created
# via the web, those tests to create a user with an instance should also be placed
# under instances. Yes this leads to code copying but it's the best way to do
# it since each test requires it's own setup and I am not fond of importing
# unit tests. -BMH
class AccountsTestCase(TestCase):

    # Test user registration
    def test_user_registration(self):
        user = User(email='testing@someemail.com', password='password')
        user.save()
        user = User.objects.filter(email="testing@someemail.com")
        # Ensure a user object exists
        self.assertTrue(len(user) > 0, 'User creation did not fail')
        # Ensure a user object is instance of User
        self.assertIsInstance(user[0], User, 'User object is of class User')
        self.assertTrue(user[0].groups.get(name='Player'), 'User object has Player group')

    # Ensure long emails will work
    def test_large_email_registration(self):
        # Ensure a user can be created with a large email address
        user = User(email='testing@thisisareallylongemailaddress.com')
        user.save()
        user = User.objects.filter(email="testing@thisisareallylongemailaddress.com")
        # Ensure a user object exists
        self.assertTrue(len(user) > 0, 'User creation did not fail')
        # Ensure a user object is instance of User
        self.assertIsInstance(user[0], User, 'User object is of class User')
        self.assertTrue(user[0].groups.get(name='Player'), 'User object has Player group')

    # Test multiple registrations
    def test_multiple_registrations(self):
        # Account 1
        user = User(email='testing@thisisareallylongemailaddress.com')
        user.save()
        user = User.objects.filter(email="testing@thisisareallylongemailaddress.com")
        
        # Account 2
        user2 = User(email='testing2@thisisareallylongemailaddress.com')
        user2.save()
        user2 = User.objects.filter(email="testing@thisisareallylongemailaddress.com")
        
        # Ensure a user object exists
        self.assertTrue(len(user) > 0, 'User creation did not fail')
        self.assertTrue(len(user2) > 0, 'User2 creation did not fail')

        # Ensure a user object is instance of User
        self.assertIsInstance(user[0], User, 'User object is of class User')
        self.assertIsInstance(user2[0], User, 'User2 object is of class User')

    # Fetch profile
    def test_user_profile(self):
        user = User(email='testing@someemail.com', password='password')
        user.save()
        # Fetch profile
        profile = user.get_profile()
        # Ensure a profile was successfully fetched
        self.assertTrue(profile, 'Profile was created successfully')
        # Ensure the profile is of UserProfile type
        self.assertIsInstance(profile, UserProfile, 'Profile is instance of UserProfile')
    
    def test_register(self):
        c = Client()
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": "testRegister@localhost.com"})
        #status_code 302 denotes a redirect but that the same URI should still be used
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        user = User.objects.filter(email="new_test@localhost.com")
        self.assertTrue(len(user) > 0, "The user was created successfully")
    
    def test_login(self):
        c = Client()
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": "testLogin@localhost.com"})
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        response = c.post("/account/login/", {"password": "pass", "email": "testLogin@localhost.com"})
        self.assertTrue(response.status_code == 200, "Loged in")
        
    def test_logout(self):
        fout = open("/home/ben/djangoOut", "w")
        c = Client()
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": "testLogout@localhost.com"})
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        response = c.post("/account/login/", {"password": "pass", "email": "testLogout@localhost.com"})
        self.assertTrue(response.status_code == 200, "Loged in")
        response = c.post("/acount/logout/")
        fout.write("%s\n" % response.content)
        self.assertTrue(response.status_code == 200, "Loged out")
    
    def test_upload(self):
        c = Client()
        fout = open("/home/ben/djangoOut", "w")
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": "testUpload@localhost.com"})

        self.assertTrue(response.status_code == 302, "User Created")
        
        response = c.post("/account/login/", {"password": "pass", "email": "testUpload@localhost.com"})
        self.assertTrue(response.status_code == 200, "Loged in")
        
        user = User.objects.get(email="testUpload@localhost.com")
        f = open("/home/ben/Desktop/Viconia.jpg", "r")
        response = c.post("/account/profile/edit/", {"avatar": f,
                                                     "user": user, "form": "updated_profile", "email": "testUpload@localhost.com",
                                                     "first_name": "new_test", "last_name": "new_test"} )
        self.assertTrue(response.status_code==302, "File uploaded")
        
        user = User.objects.get(email="testUpload@localhost.com")
        profile = user.get_profile()
        self.assertTrue(profile.avatar != None and profile.avatar != "", "Avatar filename is in the database")
        
        try:
            img = Image.open("%s%s" % (MEDIA_ROOT, profile.avatar))
        except:
            self.fail("The image at %s%s can not be found or is an invalid image" % (MEDIA_ROOT, profile.avatar))
        
        f.close()
        fout.close()
    

# Organize the Accounts test suite
def suite():
    tests = [
             'test_user_registration',
             'test_large_email_registration',
             'test_multiple_registrations',
             'test_user_profile',
             'test_register',
             'test_login',
             'test_logout',
             'test_upload'
            ]

    return unittest.TestSuite(map(AccountsTestCase, tests))
