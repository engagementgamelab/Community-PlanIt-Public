__all__ =  (
        "UserProfileEducation",
        "UserProfileGender",
        "UserProfileHowDiscovered",
        "UserProfileIncome",
        "UserProfileLivingSituation",
        "UserProfileRace",
        "UserProfileStake",
)

from django.db import models

class UserProfileOptionBase(models.Model):
    pos = models.IntegerField(blank=False, null=False)

    class Meta:
        ordering = ('pos',)
        abstract = True

class UserProfileEducation(UserProfileOptionBase):
    education = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Education option"
        verbose_name_plural = "User Profile Education options"

    def __unicode__(self):
        return self.education

class UserProfileGender(UserProfileOptionBase):
    gender = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Gender option"
        verbose_name_plural = "User Profile Gender options"

    def __unicode__(self):
        return self.gender

class UserProfileHowDiscovered(UserProfileOptionBase):
    how = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile How Discovered option"
        verbose_name_plural = "User Profile How Discovered options"

    def __unicode__(self):
        return self.how

class UserProfileIncome(UserProfileOptionBase):
    income = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Income option"
        verbose_name_plural = "User Profile Income options"

    def __unicode__(self):
        return self.income
    
class UserProfileLivingSituation(UserProfileOptionBase):
    situation = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Living Situation option"
        verbose_name_plural = "User Profile Living Situation options"

    def __unicode__(self):
        return self.situation

class UserProfileRace(UserProfileOptionBase):
    race = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Race option"
        verbose_name_plural = "User Profile Race options"

    def __unicode__(self):
        return self.race


class UserProfileStake(UserProfileOptionBase):
    """
    The stakes users hold in the community, e.g. Live, Work, Play, or Teacher,
    Administrator, Student.
    """
    stake = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Stake option"
        verbose_name_plural = "User Profile Stake options"

    def __unicode__(self):
        return self.stake
