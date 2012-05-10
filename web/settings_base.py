# -- coding: utf-8 --
import os
import sys
import re
import logging

ROOTDIR = os.path.dirname(os.path.realpath(__file__))
DIRNAME = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.abspath(DIRNAME))

#
# Standard Django settings
#
ADMIN_MEDIA_PREFIX = '/static/admin/'

#admin_tools
ADMIN_TOOLS_MEDIA_URL = '/static/'
ADMIN_TOOLS_MENU = 'web.reports.admin.ReportsMenu'

MEDIA_ROOT = os.path.join(DIRNAME, '../assets')
MEDIA_URL = '/assets/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = os.path.join(PARENT_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

ADMINS = ( ('philip.kalinsky', 'eloquentbits.com'), )
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTHENTICATION_BACKENDS = ( 'web.accounts.backends.EmailBackend', )
DATE_FORMAT = '%m/%d/%Y'
DEBUG = False
TEMPLATE_DEBUG = DEBUG
DEFAULT_FROM_EMAIL = 'noreply@communityplanit.org'

INTERNAL_IPS = ('127.0.0.1',)

# DATABASES: complete your database configuration in settings.py

EMAIL_BACKEND = 'django_mailer.smtp_queue.EmailBackend'

TEMPLATE_DIRS = (
    os.path.join(ROOTDIR, 'templates_redesign'),
    os.path.join(ROOTDIR, 'templates'),
    os.path.join(ROOTDIR, '../../parts/django-nani/hvad/templates'),
)

INSTALLED_APPS = (
    # localeurl should be first
    'localeurl',   
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    
    'web.accounts',
    'web.affiliations',
    'web.answers',
    'web.attachments',
    'web.badges',
    'web.challenges',
    'web.crowds',
    'web.comments',
    'web.core',
    'web.curator',
    'web.flags',
    'web.instances',
    'web.lists',
    'web.missions',
    'web.player_activities',
    'web.reports',
    'web.responses',
    'web.values',

    # Need this after web.admin because of test runner: 
    # it loads django admin tests by 'admin' app label first
    'django.contrib.admin',
    'django.contrib.admindocs',

    # 3rd party
    #'djcelery',
    'endless_pagination',
    'stream',
    'django_mailer',
    'django_extensions',
    'gmapsfield',
    'gmapsfield.templatetags',
    'nani',
    #'dilla',
    'rosetta',
    # django-ajax-selects
    'ajax_select',
    'django_extensions',
    #'template_repl',
    'cache_utils',
    'south',
)

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
MANAGERS = ADMINS
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MEDIA_ROOT = os.path.join(DIRNAME, '../assets')
MEDIA_URL = '/assets/'

STATIC_ROOT = os.path.join(DIRNAME, 'static_collected')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(DIRNAME, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


MIDDLEWARE_CLASSES = (
    'localeurl.middleware.LocaleURLMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'web.middleware.CurrentDomainMiddleware',
)

NOREPLY_EMAIL = 'noreply@communityplanit.org'
ROOT_URLCONF = 'web.urls'
SECRET_KEY = 'SET THIS IN settings.py'

SERIALIZATION_MODULES = {
    'yaml': "django.core.serializers.pyyaml"
} 

SERVER_EMAIL = 'noreply@communityplanit.org'

SITE_ID = 1

SESSION_COOKIE_DOMAIN = '.communityplanit.org'
#SESSION_COOKIE_PATH = '/pk.local'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'web.context_processors.site'
)

TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True


CACHES = {
    'default': {
        'BACKEND': 'cache_utils.group_backend.CacheClass',
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'cpi',
        'TIMEOUT':  60*60*24*365,
        'VERSION': 1,
    }
}

# Localization
LANGUAGE_CODE = 'en-us'
LOCALE_PATHS = (
        os.path.join(ROOTDIR, 'locale'),
)

ugettext = lambda s: s
LANGUAGES = (
  ('en-us', ugettext('English')),
  ('es', ugettext(u'Spanish')),
  ('zh-cn', ugettext(u'Chinese')),
  ('ht', ugettext(u'Haitian Creole')),
)
#django-rosetta
ROSETTA_UWSGI_AUTO_RELOAD = True
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True

#django-localeurl
LOCALE_INDEPENDENT_PATHS = (
    #re.compile('^/$'),
    re.compile('^/ajax/'),
    re.compile('^/rosetta/'),
    re.compile('^/ajax_select/'),
    re.compile('^.*/ajax/'),
    re.compile('^/comments/'),
    re.compile('^/__debug__/'),
    re.compile('^/assets/'),
    re.compile('^/accounts/logout/'),
    re.compile('^/static/'),
    re.compile('^/gr/'),
    re.compile('^/admin/'),
    re.compile('^/admin-media/'),
    re.compile('^/status/cache/'),
    re.compile('^/favicon.ico$'),
)
LOCALE_INDEPENDENT_MEDIA_URL = True
PREFIX_DEFAULT_LOCALE = True

#django-stream
# see notes in web.reports.actions
STREAM_VERBS = (
    #('challenge_created', 'created a challenge'),
    #('challenge_updated', 'updated a challenge'),
    #('challenge_accepted', 'accepted a challenge'),
    #('challenge_declined', 'declined a challenge'),
    #('challenge_deleted', 'deleted a challenge'),
    #('challenge_commented', 'commented on a challenge'),
    #('challenge_completed', 'completed a challenge'),
    #('activity_official_response_created', 'created a response'),
    #('token_spent', 'spent token'),
    #('token_reclaimed', 'reclaimed token'),

    ('crowd_created', 'create a crowd'),

    ('activity_replayed', 'replayed challenge'),
    ('activity_completed', 'completed challenge'),
    ('activity_player_submitted', 'player submitted an activity'),

    ('replied', 'replied'),
    ('liked', 'liked a comment'),
    ('commented', 'comment'),

    ('flag_awarded', 'a flag was awarded'),
    ('flag_spent', 'a flag was spent'),
    ('flag_reclaimed', 'a flag was reclaimed'),

    ('user_logged_in', 'a user logged into the system'),
)

REPORTS_RECIPIENTS = (
        'eric_gordon@emerson.edu',
        'philip.kalinsky@eloquentbits.com',
)

BRINGCPI_RECIPIENTS = ['eric_gordon@emerson.edu']

# ajax_select
# used in autocompletion
AJAX_LOOKUP_CHANNELS = {
    'affiliations': ('accounts.lookups', 'AffiliationsLookup'),
}

#django_endless_pagination
ENDLESS_PAGINATION_ADD_NOFOLLOW = True
ENDLESS_PAGINATE_PLAYERS_PER_PAGE = 16
ENDLESS_PAGINATION_PREVIOUS_LABEL = '''<div class="pagination-previous"></div>'''
ENDLESS_PAGINATION_NEXT_LABEL = '''<div class="pagination-next"></div>'''

#CommunityPlanIt uwsgi tasks settings
REBUILD_LEADERBOARD_SLEEP_SECONDS = 60*30
CRON_MAIL_SLEEP_SECONDS = 60*3
CRON_MAIL_RETRY_DEFERRED_SLEEP_SECONDS = 60*20

# celery disabled
# using uwsgi spoooler, timer decorator for now

# django-celery
#import djcelery
#djcelery.setup_loader()
#CELERY_IMPORTS = ('badges.tasks',)

#BROKER_HOST = "localhost"
#BROKER_PORT = 5672
#BROKER_USER = "guest"
#BROKER_PASSWORD = "guest"
#BROKER_VHOST = "/"

#
# Community PlanIT settings
#

# Default points/coins
DEFAULT_POINTS = 10
DEFAULT_COINS = 0


# Heatmap Threshold
# The divisor in calculating heat map regions. 
# higher number means harder to get "hot"
HEATMAP_THRESHOLD = 5

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

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(ROOTDIR, '../../log/cpi.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'request_handler': {
                'class':'django.utils.log.NullHandler',
        },

    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': { # Stop SQL debug from logging to main logger
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}


# settings can be overridden for testing; by default we use the in-memory
# sqlite database instead of PostgreSQL
if 'test' in sys.argv:
    try:
        from settings_test import *
    except ImportError:
        pass


