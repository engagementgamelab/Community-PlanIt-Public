import tempfile
import unittest

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User, Group

from PIL import Image, ImageDraw

from accounts.models import UserProfile
from core.test_fixtures import create_fixtures
from instances.models import Instance

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
        user = User.objects.filter(email="testRegister@localhost.com")
        self.assertTrue(len(user) > 0, "The user was created successfully")
    
    def test_login(self):
        c = Client()
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": "testLogin@localhost.com"})
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        response = c.post(reverse('accounts_login'), {"password": "pass", "email": "testLogin@localhost.com"})
        self.assertTrue(response.status_code == 200, "Loged in")
        
    def test_logout(self):
        c = Client()
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": "testLogout@localhost.com"})
        self.assertTrue(response.status_code == 302, "The response status denotes that the user should have been created")
        response = c.post(reverse('accounts_login'), {"password": "pass", "email": "testLogout@localhost.com"})
        self.assertTrue(response.status_code == 200, "Loged in")
        response = c.post("/account/logout/")
        self.assertTrue(response.status_code == 302, "Loged out")
    
    def test_upload(self):
        c = Client()
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": "testUpload@localhost.com"})

        self.assertTrue(response.status_code == 302, "User Created")
        
        response = c.post(reverse('accounts_login'), {"password": "pass", "email": "testUpload@localhost.com"})
        self.assertTrue(response.status_code == 200, "Logged in")
        
        user = User.objects.get(email="testUpload@localhost.com")
        image = Image.new("RGB", (75, 75))
        draw = ImageDraw.Draw(image)
        draw.rectangle(((25,25), (50, 50)), fill="#ff0000")

        f = tempfile.NamedTemporaryFile()
        image.save(f, "PNG")
        f.seek(0)

        response = c.post("/account/profile/edit/", {"avatar": f,
                                                     "user": user, "form": "updated_profile", "email": "testUpload@localhost.com",
                                                     "first_name": "new_test", "last_name": "new_test"} )
        self.assertTrue(response.status_code==302, "File upload failed")
        
        user = User.objects.get(email="testUpload@localhost.com")
        profile = user.get_profile()
        self.assertTrue(profile.avatar != None and profile.avatar != "", "Avatar filename is in the database")
        
        try:
            img = Image.open("%s%s" % (settings.MEDIA_ROOT, profile.avatar))
        except:
            self.fail("The image at %s%s can not be found or is an invalid image" % (settings.MEDIA_ROOT, profile.avatar))
    
    def test_changeGender(self):
        c = Client()
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": "testUpload@localhost.com"})
        self.assertTrue(response.status_code == 302, "User Created")
        user = User.objects.filter(email="testUpload@localhost.com")
        self.assertTrue(len(user) == 1, "User exists")
        
        response = c.post(reverse('accounts_login'), {"password": "pass", "email": "testUpload@localhost.com"})
        self.assertTrue(response.status_code == 200, "Loged in")
        
        
        response = c.post("/account/profile/edit/", {"user": user, "form": "updated_profile", "email": "testUpload@localhost.com",
                                                     "first_name": "new_test", "last_name": "new_test", "gender": "2"})
        user = UserProfile.objects.filter(user__email="testUpload@localhost.com")[0]
        self.assertTrue(user.gender.pos == 2, "The gender is correct")
    
    def test_changeLiving(self):
        c = Client()
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": "testUpload@localhost.com"})
        self.assertTrue(response.status_code == 302, "User Created")
        user = User.objects.filter(email="testUpload@localhost.com")
        self.assertTrue(len(user) == 1, "User exists")
        
        response = c.post(reverse('accounts_login'), {"password": "pass", "email": "testUpload@localhost.com"})
        self.assertTrue(response.status_code == 200, "Loged in")
        
        
        response = c.post("/account/profile/edit/", {"user": user, "form": "updated_profile", "email": "testUpload@localhost.com",
                                                     "first_name": "new_test", "last_name": "new_test", "living": "2"})
        user = UserProfile.objects.filter(user__email="testUpload@localhost.com")[0]
        self.assertTrue(user.living.pos == 2, "The living is correct")
    
    def test_changeIncome(self):
        c = Client()
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": "testUpload@localhost.com"})
        self.assertTrue(response.status_code == 302, "User Created")
        user = User.objects.filter(email="testUpload@localhost.com")
        self.assertTrue(len(user) == 1, "User exists")
        
        response = c.post(reverse('accounts_login'), {"password": "pass", "email": "testUpload@localhost.com"})
        self.assertTrue(response.status_code == 200, "Loged in")
        
        
        response = c.post("/account/profile/edit/", {"user": user, "form": "updated_profile", "email": "testUpload@localhost.com",
                                                     "first_name": "new_test", "last_name": "new_test", "income": "2"})
        user = UserProfile.objects.filter(user__email="testUpload@localhost.com")[0]
        self.assertTrue(user.income.pos == 2, "The income is correct")
    
    
    def test_changeEducation(self):
        c = Client()
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": "testUpload@localhost.com"})
        self.assertTrue(response.status_code == 302, "User Created")
        user = User.objects.filter(email="testUpload@localhost.com")
        self.assertTrue(len(user) == 1, "User exists")
        
        response = c.post(reverse('accounts_login'), {"password": "pass", "email": "testUpload@localhost.com"})
        self.assertTrue(response.status_code == 200, "Loged in")
        
        
        response = c.post("/account/profile/edit/", {"user": user, "form": "updated_profile", "email": "testUpload@localhost.com",
                                                     "first_name": "new_test", "last_name": "new_test", "education": "2"})
        user = UserProfile.objects.filter(user__email="testUpload@localhost.com")[0]
        self.assertTrue(user.education.pos == 2, "The education is correct")
        
    def test_changeRace(self):
        c = Client()
        response = c.post("/account/register/", {"password": "pass", "passwordAgain": "pass", "firstName": "new_test",
                                                  "lastName": "new_test", "email": "testUpload@localhost.com"})
        self.assertTrue(response.status_code == 302, "User Created")
        user = User.objects.filter(email="testUpload@localhost.com")
        self.assertTrue(len(user) == 1, "User exists")
        
        response = c.post(reverse('accounts_login'), {"password": "pass", "email": "testUpload@localhost.com"})
        self.assertTrue(response.status_code == 200, "Loged in")
        
        
        response = c.post("/account/profile/edit/", {"user": user, "form": "updated_profile", "email": "testUpload@localhost.com",
                                                     "first_name": "new_test", "last_name": "new_test", "race": "2"})
        user = UserProfile.objects.filter(user__email="testUpload@localhost.com")[0]
        self.assertTrue(user.race.pos == 2, "The race is correct")

class UserProfileModelTests(TestCase):
    
    def setUp(self):
        create_fixtures()
        self.test_instance = Instance.objects.untranslated().get(pk=1)
        
    def test_get_comments(self):
        profile = UserProfile.objects.get(pk=1)
        comment = profile.comments.create(instance=self.test_instance,
                                          content_object=profile,
                                          user=profile.user)
        comment.translate('ht')
        comment.message='Hi'
        comment.save()
        self.assertEqual(1, profile.get_preferred_comments().count())
        self.assertEqual(0, profile.get_english_comments().count())
        
        