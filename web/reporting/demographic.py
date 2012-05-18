from stream.models import Action

from web.accounts.models import UserProfilePerInstance, UserProfile
from web.badges.models import BadgePerPlayer
from .utils import Report

class DemographicReport(Report):
    """ -- activity report by user - 
        this report should be organized by user name and 
        - include 
            all demographic data, 
            number of log-ins, 
            flag placement, 
            badges earned, 
            number of challenges completed, 
            number of challenges created, 
            number of comments liked, 
            number of comments replied to.  """

    def run(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id')
        self.notify_subject = "Report"

        def get_stakes(profile):
            return profile.format_stakes

        def get_affiliations(profile):
            return ", ".join(profile.affils.values_list('name', flat=True))

        self.field_titles = (
                'ID', 
                'first name',
                'last name',
                'stake', 
                'affiliations', 
                'preferred language', 
                'picture', 
                'race', 
                'gender', 
                'education', 
                'income', 
                'rent/own', 
                'city/neighborhood', 
                'zip code', 
                'number of log-ins',
                'total flags spent for game', 
                'total points for game', 
                'badges earned', 
        )
        self.values_list = []

        for user_prof_per_instance in UserProfilePerInstance.objects.filter(
                                                    instance__id=self.instance_id).\
                                                exclude(
                                                    user_profile__user__is_superuser=True,
                                                    user_profile__user__is_staff=True,):

            profile =  user_prof_per_instance.user_profile
            user =  user_prof_per_instance.user_profile.user
            all_details = (
                    user_prof_per_instance.pk,
                    user.first_name,
                    user.last_name,
                    get_stakes(user_prof_per_instance),
                    get_affiliations(user_prof_per_instance),
                    user_prof_per_instance.preferred_language.name,
                    "Yes" if profile.avatar else "No",
                    profile.race.race if hasattr(profile, 'race') and profile.race is not None else "",
                    profile.gender.gender if hasattr(profile, 'gender') and profile.gender is not None else "",
                    profile.education.education if hasattr(profile, 'education') and profile.education is not None else "",
                    profile.income.income if hasattr(profile, 'income') and profile.income is not None else "",
                    profile.living.situation if hasattr(profile, 'living') and profile.living is not None else "",
                    profile.city or "",
                    profile.zip_code or "",
                    Action.objects.get_for_actor(user).filter(verb='user_logged_in').count(),
                    user_prof_per_instance.flags,
                    user_prof_per_instance.total_points,
                    ", ".join(BadgePerPlayer.objects.filter(user=user).values_list('badge__title', flat=True)),
            )
            self.values_list.append(all_details)
            #for c in profile.user.comment_set.all():
            #    values_list.append((profile.user.pk, c.message, '', '', '', ''))
        super(DemographicReport, self).run(*args, **kwargs)


