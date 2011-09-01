import random
import string
from django.conf import settings
from dilla import spam
from instances.models import Instance

#@spam.strict_handler('instances.Instance.state')
#def instance_state(record, field):
#    print 'instance_state'
#    return random.choice(string.ascii_letters)[:2].upper()

DICT_LOOKUP = {
    'en-us': settings.DICTIONARY,
    'fr': "/usr/share/dict/french",
    'de': "/usr/share/dict/german-medical",
    'ru': "/usr/share/dict/ukrainian",
}

def random_words(language_code, num):
    dictionary = DICT_LOOKUP[language_code]
    d = open(dictionary, "r").readlines()

    _random_words = \
            lambda n: " ".join([random.choice(d).lower().rstrip() \
            for i in range(n)])

    return _random_words(num)

def _random_language_code():
    lc =  random.choice([x[0] for x in settings.LANGUAGES])
    if lc == 'en':
        return 'en-us'
    return lc

@spam.strict_handler('instances.InstanceTranslation.master')
def instancetranslation_name(record, field):
    import ipdb;ipdb.set_trace()
    if not record.obj.language_code:
    	record.obj.language_code = _random_language_code()
    	record.obj.save()

@spam.strict_handler('instances.InstanceTranslation.name')
def instancetranslation_name(record, field):
    #import ipdb;ipdb.set_trace()
    if not record.obj.language_code:
    	record.obj.language_code = _random_language_code()
    	record.obj.save()

    return random_words(record.obj.language_code, 3)

@spam.strict_handler('instances.InstanceTranslation.language_code')
def instancetranslation_language_code(record, field):
    if not record.obj.language_code:
    	return _random_language_code()
    return record.obj.language_code

@spam.strict_handler('instances.Instance.name')
def instance_name(record, field):
    return random.choice(string.ascii_letters)

