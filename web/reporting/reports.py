from stream.models import Action

from web.accounts.models import UserProfilePerInstance, UserProfile
from web.badges.models import BadgePerPlayer
from .utils import Report


def get_demographic_field_titles():
    return (
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
    )

def get_demographic_details(user_prof_per_instance, profile, user, instance_id):

    def get_stakes(profile):
        return profile.format_stakes

    def get_affiliations(profile):
        return ", ".join(profile.affils.values_list('name', flat=True))

    return (
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
    )

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
        self.notify_subject = "Demographic-Report"


        self.field_titles = get_demographic_field_titles() + (
                'number of log-ins',
                'total flags spent for game', 
                'total points for game', 
                'badges earned', 
                'challenge completed count',
                'challenges created count',
                'comments liked count',
                'comments replied to count',
        )
        self.values_list = []

        for user_prof_per_instance in UserProfilePerInstance.objects.filter(
                                                    instance__id=self.instance_id).\
                                                exclude(
                                                    user_profile__user__is_superuser=True,
                                                    user_profile__user__is_staff=True,):

            profile =  user_prof_per_instance.user_profile
            user =  user_prof_per_instance.user_profile.user
            all_details = get_demographic_details(user_prof_per_instance, profile, user, self.instance_id) + (
                    Action.objects.get_for_actor(user).filter(verb='user_logged_in').count(),
                    user_prof_per_instance.flags,
                    user_prof_per_instance.total_points,
                    ", ".join(BadgePerPlayer.objects.filter(user=user).values_list('badge__title', flat=True)),
                    Action.objects.get_for_actor(user).filter(verb='activity_completed', target_instance__pk=self.instance_id).count(),
                    Action.objects.get_for_actor(user).filter(verb='activity_player_submitted', target_instance__pk=self.instance_id).count(),
                    Action.objects.get_for_actor(user).filter(verb='liked', target_comment__instance__pk=self.instance_id).count(),
                    Action.objects.get_for_actor(user).filter(verb='commented', target_comment__instance__pk=self.instance_id).count(),
            )
            self.values_list.append(all_details)
        super(DemographicReport, self).run(*args, **kwargs)


class LoginActivityReport(Report):
    """
        -- activity time by user - 
        this report should include user name and demographic data and when they logged in.  """


    def run(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id')
        self.notify_subject = "Login-Activity-Report"


        self.field_titles = get_demographic_field_titles() + (
                'number of log-ins',
                'login dates/times',
        )
        self.values_list = []

        for user_prof_per_instance in UserProfilePerInstance.objects.filter(
                                                    instance__id=self.instance_id).\
                                                exclude(
                                                    user_profile__user__is_superuser=True,
                                                    user_profile__user__is_staff=True,):

            profile =  user_prof_per_instance.user_profile
            user =  user_prof_per_instance.user_profile.user


            login_actions = Action.objects.get_for_actor(user).filter(verb='user_logged_in')

            datetimes = login_actions.values_list('datetime', flat=True)

            all_details = get_demographic_details(user_prof_per_instance, profile, user, self.instance_id) + (
                    login_actions.count(),
                    ", ".join([dt.strftime('%Y-%m-%d-%H-%M') for dt in datetimes]),
            )
            self.values_list.append(all_details)
        super(LoginActivityReport, self).run(*args, **kwargs)


