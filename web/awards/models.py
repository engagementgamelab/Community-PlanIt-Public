#from stream import utils as stream_utils
from django.db import models
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
#from django.db.models.signals import post_save
#from django.dispatch import receiver

#from web.comments.models import Comment

"""
All Awards (Badges) should be treated less as a reputation system and more as a bonus system.
So every Award should come with a coin bonus.

All Awards are mission-specific. The bonus coins I earn from Awards should go into my coin pot for the mission the Award was earned in.

Users have the ability to earn the same Award in each mission (i.e. If I earn the "firebrand" award in Mission 1, I can also win it again in Mission 2).

    1) Making your very first comment (explorer)
    2) Being a top 10 coin-earner when the mission ends (trailblazer)
    3) Being #1 coin earner when the mission ends - (visionary)
    4) Receiving 5 likes in a mission (celebrity)
    5) Receiving 12 likes in a mission (superstar)
    6) Receiving 3 comments on a single response (provocateur)
    7) Receiving 7 comments on a single response. (firebrand)
    8) Making 5 comments in a mission (commentator)
    9) Making 12 comments in a mission (pontificator)
    10) Getting all trivia barriers for a mission correct without using any lifelines (smarty pants)
    11) Posing 3 challenges (instigator)
    12) Having 5 people respond to a challenge you've posed. (mobilizer)
    13) Having 10 people respond to a challenge you've posed. (rabble-rouser)

    1) submitting comments.             instance - comments.Comment
    2) earning coins.                   instance - challenges.Answer
    3) receiving likes                  instance - xxx.Like?
    4) receiving comments on answers    instance - comments.Comment
    5) answering trivia barriers correctly 
        without using lifelines         instance - challenges.Answer
    6) posing challenges                instance - challenges.Challenge
    7) having players answer your 
        challenges                      instance - challenges.Challenge
"""


class Award(models.Model):

    MOVER_SHAKER, HOMETOWN_HERO, COMMUNITY_BUILDER, \
    PROVOCATEUR, VISIONARY, EMPATHIZER, LOCAL_SAGE, \
    CROWDSOURCER, CROWDSURFER, NETWORKER, LOCAL_LEADER = xrange(1,12)
    AWARD_TYPES = (
        (MOVER_SHAKER, _("Mover and Shaker")),
        (HOMETOWN_HERO, _("Hometown Hero")),
        (COMMUNITY_BUILDER, _("Community Builder")),
        (PROVOCATEUR, _("Provocateur")),
        (VISIONARY, _("Visionary")),
        (EMPATHIZER, _("Empathizer")),
        (LOCAL_SAGE, _("Local Sage")),
        (CROWDSOURCER, _("Crowdsourcer")),
        (CROWDSURFER, _("Crowdsurver")),
        (NETWORKER, _("Networker")),
        (LOCAL_LEADER, _("Local Leader")),
    )
    slug = models.SlugField(_("Slug"))
    title = models.CharField(_("Title"), max_length=255)
    name = models.CharField(max_length="100")
    description = models.TextField()
    type = models.IntegerField(_("Award Type"), unique=True, choices=AWARD_TYPES, default=0)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.name)[:30]
        super(Award, self).save()


class AwardRulesBase(object):
	award_type = Award.COMMUNITY_BUILDER


class CommunityBuilderRules(AwardRulesBase):
	COMMENTS_PER_LEVEL = 15
	TOTAL_LEVELS = 3


class PlayerAward(models.Model):
    award = models.ForeignKey(Award)
    level = models.IntegerField(default=1)

    def increment_level(self, n=1):
        self.level+=n

#@receiver(post_save, sender=Comment, dispatch_uid='cpi-badges')
#def my_callback(sender, **kwargs):
#    print "comment created!"


# **** sql to add column to stream_action table
#ALTER TABLE stream_action ADD COLUMN action_object_badgeperplayer_id integer;
#stream_utils.register_action_object(BadgePerPlayer)

