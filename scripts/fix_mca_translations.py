#!/usr/bin/env python

from nani.utils import get_translation_aware_manager

from player_activities.models import *

def fix_mca_translations():
    player_activities = PlayerActivity.objects.all().order_by('pk') # filter(id=3260)
    tam = get_translation_aware_manager(MultiChoiceActivity)
    for activity in player_activities:
        english = tam.filter(activity=activity, language_code='en-us')
        english_list = list(english)
        spanish = tam.filter(activity=activity, language_code='es')
        spanish_list = list(spanish)
        creole = tam.filter(activity=activity, language_code='ht')
        creole_list = list(creole)

        for i, choice in enumerate(english):
            #print "CHOICE %s/%s BEFORE TRANSLATION:" % (choice.activity, choice.pk)
            #print [(c.pk, c.language_code, c.value) for c in choice.translations.all()]

            try:
                choice.translate('es')
                choice.value = spanish_list[i].translations.all()[0].value
                choice.save()
            except Exception, e:
                print "ACTIVITY %s ('%s') LACKS SPANISH TRANSLATION" % (activity.pk, activity)

            try:
                choice.translate('ht')
                choice.value = creole_list[i].translations.all()[0].value
                choice.save()
            except Exception, e:
                print "ACTIVITY %s ('%s') LACKS CREOLE TRANSLATION" % (activity.pk, activity)

            #print "CHOICE %s/%s AFTER TRANSLATION:" % (choice.activity, choice.pk)
            #print [(c.pk, c.language_code, c.value) for c in choice.translations.all()]

        #print "DELETING CREOLE TRANSLATIONS: ", creole
        for c in creole:
            c.delete()
        #print "DELETING SPANISH TRANSLATIONS: ", spanish
        for s in spanish:
            s.delete()
