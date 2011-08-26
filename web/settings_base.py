# -- coding: utf-8 --
import os
import sys
import re

ROOTDIR = os.path.dirname(os.path.realpath(__file__))

#
# Standard Django settings
#
ADMIN_MEDIA_PREFIX = '/admin-media/'
ADMINS = ( ('Benedict Holland', 'sheepskin505@gmail.com'), )
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTHENTICATION_BACKENDS = ( 'web.accounts.backends.EmailBackend', )
DEBUG = False
DEFAULT_FROM_EMAIL = 'noreply@communityplanit.org'
DIRNAME = os.path.dirname(__file__)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
} 

# DATABASES: complete your database configuration in settings.py

EMAIL_BACKEND = 'django_mailer.smtp_queue.EmailBackend'

INSTALLED_APPS = (
    # localeurl should be first
    'localeurl',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',

    'web',
    'web.accounts',
    'web.admin',
    'web.answers',
    'web.attachments',
    'web.challenges',
    'web.comments',
    'web.curator',
    'web.flags',
    'web.instances',
    'web.lists',
    'web.missions',
    'web.player_activities',
    'web.reports',
    'web.responses',
    'web.values',

    # 3rd party
    'django_mailer',
    'django_extensions',
    'gmapsfield',
    'gmapsfield.templatetags',
    'nani',
    'rosetta',
    'south',
)

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
MANAGERS = ADMINS
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MEDIA_ROOT = os.path.join(DIRNAME, '../assets')
MEDIA_URL = '/assets/'

MIDDLEWARE_CLASSES = (
    'localeurl.middleware.LocaleURLMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

NOREPLY_EMAIL = 'noreply@communityplanit.org'
ROOT_URLCONF = 'web.urls'
SECRET_KEY = 'SET THIS IN settings.py'

SERIALIZATION_MODULES = {
    'yaml': "django.core.serializers.pyyaml"
} 

SERVER_EMAIL = 'noreply@communityplanit.org'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SITE_ID = 1

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

TEMPLATE_DEBUG = True
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True

# Localization
LANGUAGE_CODE = 'en-us'
LOCALE_PATHS = (
        os.path.join(ROOTDIR, '../locale'),
)

ugettext = lambda s: s
LANGUAGES = (
  ('en', ugettext('English')),
  ('es', ugettext(u'Spanish')),
  ('ht', ugettext(u'Haitian Creole')),
)
#django-localeurl
LOCALE_INDEPENDENT_PATHS = (
    #re.compile('^/$'),
    re.compile('^/ajax/'),
    re.compile('^/assets/'),
    re.compile('^/admin-media/'),
    re.compile('^/favicon.ico$'),
)
LOCALE_INDEPENDENT_MEDIA_URL = True
PREFIX_DEFAULT_LOCALE = True


#
# Community PlanIT settings
#

# Default points/coins
DEFAULT_POINTS = 10
DEFAULT_COINS = 0

#
# South settings
#
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

#
# Google Maps Field settings 
#
GMAP_DEFAULT = [42.355241376822725,-71.06010156250015] # Boston
GMAP_JQUERY = '/assets/3pty/js/jquery-1.4.4.min.js'

# settings can be overridden for testing; by default we use the in-memory
# sqlite database instead of PostgreSQL
if 'test' in sys.argv:
    try:
        from settings_test import *
    except ImportError:
        pass


