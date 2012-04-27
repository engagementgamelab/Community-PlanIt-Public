import os.path

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
#from django.db.models.signals import post_save
#from django.dispatch import receiver
from django.utils.translation import get_language

from nani.models import TranslatableModel, TranslatedFields
from nani.manager import TranslationManager

from web.comments.models import Comment

def determine_path(instance, filename):
    return os.path.join('uploads/cities/', str(instance.domain), filename)



class Badge(TranslatableModel):

    BADGE_MOVER_SHAKER, BADGE_HOMETOWN_HERO, BADGE_COMMUNITY_BUILDER, \
    BADGE_PROVOCATEUR, BADGE_VISIONARY, BADGE_EMPATHIZER, BADGE_LOCAL_SAGE, \
    BADGE_CROWDSOURCER, BADGE_CROWDSURFER, BADGE_NETWORKER, BADGE_LOCAL_LEADER = xrange(1,12)
    BADGE_TYPES = (
        (BADGE_MOVER_SHAKER, _("Mover and Shaker")),
        (BADGE_HOMETOWN_HERO, _("Hometown Hero")),
        (BADGE_COMMUNITY_BUILDER, _("Community Builder")),
        (BADGE_PROVOCATEUR, _("Provocateur")),
        (BADGE_VISIONARY, _("Visionary")),
        (BADGE_EMPATHIZER, _("Empathizer")),
        (BADGE_LOCAL_SAGE, _("Local Sage")),
        (BADGE_CROWDSOURCER, _("Crowdsourcer")),
        (BADGE_CROWDSURFER, _("Crowdsurver")),
        (BADGE_NETWORKER, _("Networker")),
        (BADGE_LOCAL_LEADER, _("Local Leader")),
    )
    slug = models.SlugField(_("Slug"))
    title = models.CharField(_("Title"), max_length=255)
    type = models.IntegerField(_("Badge Type"), choices=BADGE_TYPES, default=0)

    translations = TranslatedFields(
        name = models.CharField(max_length="100"),
        description = models.TextField(),
        #meta = {'get_latest_by': 'start_date'}
    )

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.name)[:30]
        super(Badge, self).save()


class BadgeRulesBase(object):
	badge_type = Badge.BADGE_COMMUNITY_BUILDER


class CommunityBuilderRules(BadgeRulesBase):
	COMMENTS_PER_LEVEL = 15
	TOTAL_LEVELS = 3


class BadgePerPlayer(models.Model):
    badge = models.ForeignKey(Badge)
    user = models.ForeignKey(User)
    level = models.IntegerField(default=1)

    def increment_level(self, n=1):
        self.level+=n

    class Meta:
        unique_together = (badge, user,)


#@receiver(post_save, sender=Comment, dispatch_uid='cpi-badges')
#def my_callback(sender, **kwargs):
#    print "comment created!"



