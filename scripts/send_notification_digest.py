#!/usr/bin/env python

#
# For each active instance, sends notifications to users who have indicated
# they wish to receive mail.
#

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.template import Context, loader
from django.utils import translation
from django.utils.translation import gettext as _

from django.contrib.sites.models import Site

from web.accounts.models import UserProfile, Notification
from web.instances.models import Instance

text_template = loader.get_template('accounts/email/notifications.txt')
html_template = loader.get_template('accounts/email/notifications.html')

supported_languages = dict(settings.LANGUAGES)

for instance in Instance.objects.active():
    for user_profile in instance.user_profiles.filter(receive_email=True, user__is_active=True).order_by('preferred_language'):
        if user_profile.user.notifications.unread().count() > 0:
            language = settings.LANGUAGE_CODE
            if user_profile.preferred_language != language and user_profile.preferred_language in supported_languages:
                language = user_profile.preferred_language
            translation.activate(language)
            context = {
                'instance': instance,
                'user_profile': user_profile,
                'site': Site.objects.get_current()
            }
            subject = _('Community PlanIt Notifications')
            html_content = html_template.render(Context(context))
            text_content = text_template.render(Context(context))

            sender = settings.NOREPLY_EMAIL
            recipients = [user_profile.email or user_profile.user.email]
            message = EmailMultiAlternatives(subject, text_content, sender, recipients)
            message.attach_alternative(html_content, "text/html")
            message.send()

            user_profile.user.notifications.unread().update(read=True)
