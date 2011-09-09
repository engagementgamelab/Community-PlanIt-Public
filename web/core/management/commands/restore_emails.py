from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Store all User.email to UserProfile.email'
    
    def handle(self, *args, **options):
        users = User.objects.all()
        import ipdb
        ipdb.set_trace()
        for user in users:
            try:
                profile = user.get_profile()
                if isinstance(profile, UserProfile):
                    profile.email = user.email
                    profile.save()
            except UserProfile.DoesNotExist:
                pass
                
        print 'All emails were restored'
    