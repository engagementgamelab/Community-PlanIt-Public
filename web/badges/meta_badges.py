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

import badges

class Explorer(badges.MetaBadge):
    id = "explorer"
    model = Comment
    one_time_only = True

    title = "Explorer"
    description = "Making your very first comment"
    level = "1"

    #def get_user(self, instance):
    #    return instance.user

    #def check_comment_count(seelf, instance):
    #    challenge = instance.comment


class Trailblazer(badges.MetaBadge):
    id = "Trailblazer"
    model = Comment
    one_time_only = True

    title = "Trailblazer"
    description = "Being a top 10 coin-earner when the mission ends"
    level = "1"

    #def get_user(self, instance):
    #    return instance.user
