import os
import random
import string
from django.conf import settings
from django.template.defaultfilters import slugify
from dilla import spam
from instances.models import Instance

#@spam.strict_handler('instances.Instance.state')
#def instance_state(record, field):
#    print 'instance_state'
#    return random.choice(string.ascii_letters)[:2].upper()

DICT_LOOKUP = {
    'en-us': settings.DICTIONARY,
    'en': settings.DICTIONARY,
    'fr': "french",
    'ht': "french",
    'es': "spanish",
    'ru': "ukrainian",
}

def random_words(language_code='en-us', paragraph=False, num=5):
    ignore_trans = True

    if ignore_trans:
        dictionary = settings.DICTIONARY
    else:
        if language_code not in ['en-us', 'en']:
            dictionary = os.path.join('/usr/share/dict/', DICT_LOOKUP[language_code])
        else:
            dictionary = settings.DICTIONARY

    try:
        d = open(dictionary, "r").readlines()
    except IOError:
        raise Exception("Dictionary not found for language code: %s" % language_code)

    _random_words = \
            lambda n: " ".join([random.choice(d).lower().rstrip() \
            for i in range(n)])

    if paragraph == True:
        _random_paragraph = lambda: _random_words(30).capitalize()
        _random_paragraphs = lambda n: \
                ".\n\n".join([_random_paragraph() for i in range(n)])
        return _random_paragraphs(num)

    return _random_words(num) #.decode('iso-8859-1').encode('utf-8')

def _random_language_code():
    lc =  random.choice([x[0] for x in settings.LANGUAGES])
    #if lc == 'en':
    #    return 'en-us'
    return lc

def random_email():
    return "%s@%s.%s" % ( \
             slugify(random_words(num=1)),
             slugify(random_words(num=1)),
             random.choice(["com", "org", "net", "gov", "eu"])
             )


@spam.strict_handler('instances.InstanceTranslation.master')
def instancetranslation_name(record, field):
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

