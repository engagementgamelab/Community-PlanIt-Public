import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import email_re
from django.utils.translation import ugettext as _
from django.template import Context, loader
from web.instances.models import Instance

class Command(BaseCommand):
    def handle(self, *args, **options):
        tmpl = loader.get_template('missions/email/overview.html')

        for instance in Instance.objects.active():
            data = {
                'instance': instance,
            }

            user_profiles = instance.user_profiles.order_by("-totalPoints")
            if user_profiles.count() > 0:
                data['first_place'] = user_profiles[0]

            print data

            for user_profile in instance.user_profiles.filter(user__is_active=True):
                user = user_profile.user
                if email_re.search(user.email or ''):
                    data['user'] = user
                    body = tmpl.render(Context(data))
                    send_mail(_('Community PlanIT Weekly Mission Update'), body, settings.NOREPLY_EMAIL, [user.email])
