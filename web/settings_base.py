import os
import sys

#
# Standard Django settings
#
ADMIN_MEDIA_PREFIX = '/admin-media/'
ADMINS = ( ('Benedict Holland', 'sheepskin505@gmail.com'), )
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTHENTICATION_BACKENDS = ( 'web.accounts.backends.EmailBackend', )
DEBUG = False
DIRNAME = os.path.dirname(__file__)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
} 

# DATABASES: complete your database configuration in settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

INSTALLED_APPS = (
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
    'web.prompts',
    'web.reports',
    'web.responses',
    'web.values',

    # 3rd party
    'gmapsfield',
    'gmapsfield.templatetags',
    'south',
)

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
MANAGERS = ADMINS
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MEDIA_ROOT = os.path.join(DIRNAME, '../assets')
MEDIA_URL = '/assets/'

MIDDLEWARE_CLASSES = (
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


