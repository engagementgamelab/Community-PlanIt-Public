import unittest
from django.test import TestCase
from django.contrib.auth.models import User, Group
from web.accounts.models import UserProfile
from django.test.client import Client

# For testing Accounts
class AccountsTestCase(TestCase):

    TEST_HOST = "127.0.0.1"
    TEST_PORT = 8080
    
    

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
                                                  "lastName": "new_test", "email": "new_test@localhost.com"})
        #status_code 302 denotes a redirect but that the same URI should still be used
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        user = User.objects.filter(email="new_test@localhost.com")
        self.assertTrue(len(user) > 0, "The user was created successfully")

    #TODO: it would be nice to test login, logout and change password but this is very difficult since
    #it requires session keys.   

# Organize the Accounts test suite
def suite():
    tests = [
             'test_user_registration',
             'test_large_email_registration',
             'test_multiple_registrations',
             'test_user_profile',
             'test_register',
            ]

    return unittest.TestSuite(map(AccountsTestCase, tests))
