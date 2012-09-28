import os
import sys
import re
import logging

ROOTDIR = os.path.dirname(os.path.realpath(__file__))
DIRNAME = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(os.path.abspath(DIRNAME))

ADMIN_MEDIA_PREFIX = '/static/admin/'

# admin_tools
#ADMIN_TOOLS_MEDIA_URL = '/static/'
# ADMIN_TOOLS_MENU = 'web.reporting.admin.ReportsMenu'

MEDIA_ROOT = os.path.join(DIRNAME, '../assets')
MEDIA_URL = '/assets/'

STATIC_ROOT = os.path.join(DIRNAME, 'static_collected')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(DIRNAME, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = (
    'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
)

ADMINS = ( ('philip.kalinsky', 'eloquentbits.com'), )
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTHENTICATION_BACKENDS = (
    'web.accounts.backends.EmailBackend',
    'socialregistration.contrib.facebook.auth.FacebookAuth',
    'django_rules.backends.ObjectPermissionBackend',
)
DATE_FORMAT = '%m/%d/%Y'
DEBUG = False
TEMPLATE_DEBUG = DEBUG
DEFAULT_FROM_EMAIL = 'noreply@communityplanit.org'

INTERNAL_IPS = ('127.0.0.1',)

# DATABASES: complete your database configuration in settings.py

EMAIL_BACKEND = 'django_mailer.smtp_queue.EmailBackend'

TEMPLATE_DIRS = (
    os.path.join(ROOTDIR, 'templates'),
    #os.path.join(ROOTDIR, '../../parts/django-nani/hvad/templates'),
    #'/var/local/buildout/eggs/django_mptt-0.5.2-py2.7.egg/mptt/templates',
)

INSTALLED_APPS = (
    'grappelli',
    'filebrowser',
    'django_su',

    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.comments',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'web.accounts',
    'web.affiliations',
    'web.attachment_types',
    #'web.badges',
    'web.core',
    'web.player_comments',
    'web.curator',
    'web.flags',
    'web.instances',
    'web.lists',
    'web.missions',
    'web.challenges',
    'web.causes',
    'web.reporting',

    # Need this after web.admin because of test runner: 
    # it loads django admin tests by 'admin' app label first
    'django.contrib.admin',
    'django.contrib.admindocs',

    # 3rd party
    #'djcelery',
    'polymorphic_tree',
    'polymorphic',
    'mptt',
    #'hvad',
    #'stream',
    'attachments',
    'django_mailer',
    'gmapsfield',
    'gmapsfield.templatetags',
    'rosetta',
    'sorl.thumbnail',
    'ajax_select',
    'django_rules',
    'django_extensions',
    'socialregistration',
    'socialregistration.contrib.facebook',
    #'template_repl',
    'cache_utils',
    'south',
)

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
MANAGERS = ADMINS
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MIDDLEWARE_CLASSES = (
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    #'web.middleware.CurrentDomainMiddleware',
)

NOREPLY_EMAIL = 'noreply@communityplanit.org'
ROOT_URLCONF = 'web.urls'
SECRET_KEY = 'SET THIS IN settings.py'

SERIALIZATION_MODULES = {
    'yaml': "django.core.serializers.pyyaml"
} 

SERVER_EMAIL = 'noreply@communityplanit.org'

SITE_ID = 1

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    #'web.context_processors.game_nav',
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
)

#comments
COMMENTS_APP = 'web.player_comments'

#django-rosetta
ROSETTA_UWSGI_AUTO_RELOAD = True
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True

#django-grappelli
GRAPPELLI_ADMIN_TITLE = "CommunityPlanIt CMS"

#django-stream
# see notes in web.reports.actions
STREAM_VERBS = (

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

    ('award_received', 'player received a award'),
)

BRINGCPI_RECIPIENTS = ['eric_gordon@emerson.edu']

# ajax_select
# used in autocompletion
AJAX_LOOKUP_CHANNELS = {
    'affiliations': ('accounts.lookups', 'AffiliationsLookup'),
    'django_su': dict(model='auth.user', search_field='username'),
}

REPORTS = {
        'demographic' : ('web.reporting.reports', 'DemographicReport'),
        'login_activity' : ('web.reporting.reports', 'LoginActivityReport'),
        'challenge_activity' : ('web.reporting.reports', 'ChallengeActivityReport'),
        'mission' : ('web.reporting.reports', 'MissionReport'),
}

REPORTS_RECIPIENTS = (
        'eric_gordon@emerson.edu',
        'philip.kalinsky@eloquentbits.com',
)


# celery disabled
# using uwsgi spoooler, timer decorator for now

# django-celery
# import djcelery
# djcelery.setup_loader()
# CELERY_IMPORTS = ('badges.tasks',)

# BROKER_HOST = "localhost"
# BROKER_PORT = 5672
# BROKER_USER = "guest"
# BROKER_PASSWORD = "guest"
# BROKER_VHOST = "/"
  
#
# Community PlanIT settings
#

# Heatmap Threshold
# The divisor in calculating heat map regions. 
# higher number means harder to get "hot"
HEATMAP_THRESHOLD = 2

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


