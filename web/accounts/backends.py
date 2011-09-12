from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.core.validators import email_re
from accounts.models import UserProfile

# Custom backend to provide email authentication instead of traditional
# username/password combination.
class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        # Passed username argument could potentially be a username created via
        # createsuperuser which will not have an associated email address.  In order
        # to allow these users to login must test for email address separately.
        if email_re.search(username):
            try:
                user_profile = UserProfile.objects.get(email=username)
                user = user_profile.user                
            except UserProfile.DoesNotExist:
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:        
                    return None
        # Username did not validate to email address test for username
        else:
            try:
                # There is no feasible reason why a non-staff or superuser would log in
                # with their generated hash username.  To deter foul play, limiting access
                # to only those with proper credentials.                
                user = User.objects.get(username=username)
                if not user.is_staff or not user.is_superuser:
                    return None
            except User.DoesNotExist:
                return None

        # After user has been located need to ensure a valid password was provided.
        if user and user.check_password(password):
            return user
