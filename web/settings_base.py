# -- coding: utf-8 --
import os
import sys
import re
import logging

ROOTDIR = os.path.dirname(os.path.realpath(__file__))
DIRNAME = os.path.dirname(__file__)

#
# Standard Django settings
#
ADMIN_MEDIA_PREFIX = '/static/admin/'

#admin_tools
ADMIN_TOOLS_MEDIA_URL = '/static/'
ADMIN_TOOLS_MENU = 'web.reports.admin.ReportsMenu'

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
    # os.path.join(ROOTDIR, 'templates_redesign'),
    os.path.join(ROOTDIR, 'templates')
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

    'accounts',
    'answers',
    'attachments',
    'challenges',
    'crowds',
    'comments',
    'core',
    'curator',
    'flags',
    'instances',
    'lists',
    'missions',
    'player_activities',
    'reports',
    'responses',
    'values',

    # Need this after web.admin because of test runner: 
    # it loads django admin tests by 'admin' app label first
    'django.contrib.admin',
    'django.contrib.admindocs',

    # 3rd party
    'djcelery',
    'stream',
    'django_mailer',
    'django_extensions',
    'gmapsfield',
    'gmapsfield.templatetags',
    'nani',
    #'dilla',
    'rosetta',
    'django_extensions',
    'template_repl',
    'south',
)

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
SESSION_COOKIE_DOMAIN = '.communityplanit.org'
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
    'web.middleware.CurrentDomainMiddleware',
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
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
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
        'TIMEOUT': 300,
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
  ('ht', ugettext(u'Haitian Creole')),
  ('es', ugettext(u'Spanish')),
)
#django-localeurl
LOCALE_INDEPENDENT_PATHS = (
    #re.compile('^/$'),
    re.compile('^/ajax/'),
    re.compile('^/comments/'),
    re.compile('^/__debug__/'),
    re.compile('^/assets/'),
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
    ('challenge_created', 'created a challenge'),
    ('challenge_updated', 'updated a challenge'),
    ('challenge_accepted', 'accepted a challenge'),
    ('challenge_declined', 'declined a challenge'),
    ('challenge_deleted', 'deleted a challenge'),
    ('challenge_commented', 'commented on a challenge'),
    ('challenge_completed', 'completed a challenge'),

    ('crowd_created', 'create a crowd'),

    ('activity_official_response_created', 'created a response'),

    ('activity_replayed', 'replayed activity'),
    ('activity_completed', 'completed activity'),

    ('token_spent', 'spent token'),
    ('token_reclaimed', 'reclaimed token'),

    ('replied', 'replied'),
    ('liked', 'liked a comment'),
    ('commented', 'comment'),
)


REPORTS_RECIPIENTS = (
        'eric_gordon@emerson.edu',
        'philip.kalinsky@eloquentbits.com',
)

# django-celery
import djcelery
djcelery.setup_loader()

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"


#debug-toolbar
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS' : False,
}

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


