from django.core.mail import send_mail
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import email_re
from django.utils.translation import ugettext as _
from django.template import Context, loader

from web.instances.models import Instance
from web.accounts.models import UserProfilePerInstance

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        tmpl = loader.get_template('accounts/email/notifications.txt')
        cnt = 0
        for instance in Instance.objects.current():
            context = {
                'instance': instance,
            }
            for user_prof_per_instance in UserProfilePerInstance.objects.filter(
                                                        instance=instance, 
                                                        user_profile__receive_email=True,
                                                        user_profile__user__is_active=True,
                                                        ).filter(user_profile__user__pk=1220):
                if user_prof_per_instance.user_profile.user.notifications.unread().count() == 0:
                    continue
                context['user_prof_per_instance'] = user_prof_per_instance
                recipient = user_prof_per_instance.user_profile.email
                log.debug("sending digest to: %s at %s" % (user_prof_per_instance, recipient))
                if email_re.search(user_prof_per_instance.user_profile.email or ''):
                    body = tmpl.render(Context(context))
                    log.debug(body)
                    send_mail(_('Community PlanIT Daily digest'), 
                                    body, 
                                    settings.NOREPLY_EMAIL, 
                                    [ recipient ]
                    )
                    cnt+=1

        log.debug("done with todays digest emails. %s emails sent out." % cnt)



