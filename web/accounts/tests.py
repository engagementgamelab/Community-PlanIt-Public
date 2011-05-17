import unittest
from django.test import TestCase
from django.contrib.auth.models import User, Group
from web.accounts.models import UserProfile

# For testing Accounts
class AccountsTestCase(TestCase):

    # Test user registration
    def test_user_registration(self):
        user = User(email='tim@someemail.com', password='password')
        user.save()
        # Ensure a user object exists
        self.assertTrue(user, 'User creation did not fail')
        # Ensure a user object is instance of User
        self.assertIsInstance(user, User, 'User object is of class User')
        self.assertTrue(user.groups.get(name='Player'), 'User object has Player group')

    # Ensure long emails will work
    def test_large_email_registration(self):
        # Ensure a user can be created with a large email address
        user = User(email='tim@thisisareallylongemailaddress.com')
        user.save()
        # Ensure a user object exists
        self.assertTrue(user, 'User creation did not fail')
        # Ensure a user object is instance of User
        self.assertIsInstance(user, User, 'User object is of class User')

    # Test multiple registrations
    def test_multiple_registrations(self):
        # Account 1
        user = User(email='tim@thisisareallylongemailaddress.com')
        user.save()

        # Account 2
        user2 = User(email='tim@thisisareallylongemailaddress2.com')
        user2.save()

        # Ensure a user object exists
        self.assertTrue(user, 'User creation did not fail')
        self.assertTrue(user2, 'User2 creation did not fail')

        # Ensure a user object is instance of User
        self.assertIsInstance(user, User, 'User object is of class User')
        self.assertIsInstance(user2, User, 'User2 object is of class User')

    # Fetch profile
    def test_user_profile(self):
        user = User(email='tim@someemail.com', password='password')
        user.save()
        # Fetch profile
        profile = user.get_profile()
        # Ensure a profile was successfully fetched
        self.assertTrue(profile, 'Profile was created successfully')
        # Ensure the profile is of UserProfile type
        self.assertIsInstance(profile, UserProfile, 'Profile is instance of UserProfile')

# Organize the Accounts test suite
def suite():
    tests = [
             'test_user_registration',
             'test_large_email_registration',
             'test_multiple_registrations',
             'test_user_profile',
            ]

    return unittest.TestSuite(map(AccountsTestCase, tests))
