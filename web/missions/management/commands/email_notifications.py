import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import email_re
from django.utils.translation import ugettext as _
from django.template import Context, loader
from web.accounts.models import UserProfile
from web.instances.models import Instance
from web.missions.models import Mission

class Command(BaseCommand):
    def handle(self, *args, **options):
        tmpl = loader.get_template('missions/email/overview.html')

        for instance in Instance.objects.all():
            if instance.is_active():
                users = UserProfile.objects.filter(instance=instance)
                missions = Mission.objects.filter(instance=instance)
                past_missions = missions.past()

                past = past_missions[len(past_missions)-1]
                current = missions.current()[0]

                first_place = users.order_by("-points")[0]

                for user in users:
                    body = tmpl.render(Context({ 'past': past, 'current': current, 'users': users, 'first_place': first_place, 'user': user }))
                    if email_re.search(user.email or ''):
                        send_mail(_('Community PlanIT Weekly Mission Update'), body, settings.NOREPLY_EMAIL, [user.email])
