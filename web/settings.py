# -- coding: utf-8 --
# Manage different settings
import os
import re
from ConfigParser import RawConfigParser

ROOTDIR = os.path.dirname(os.path.realpath(__file__))

config = RawConfigParser()

# dev/staging/prod constants
DEVELOPMENT = 'thinkpad'
STAGING = 've.g6c82qm2.vesrv.com'
PRODUCTION = 'communityplanit.org'

# Toggle based on hostname
import socket
host = socket.gethostname()
config.read(os.path.join(ROOTDIR, '../config/development.ini'))

# General settings
DEBUG = config.getboolean('general', 'DEBUG')
TEMPLATE_DEBUG = DEBUG
SITE_ID = 1
SECRET_KEY = config.get('general', 'SECRET_KEY')

# Users & Admins
ADMINS = ( ('bholland', 'sheepskin505@gmail.com'), )
MANAGERS = ADMINS
LOGIN_URL = '/account/login'

# Data & session storage
#Use when testing out the web site once the database has been
#more or less solidified
DATABASES = {
    'default': {
        'ENGINE': config.get('storage', 'ENGINE'),
        'NAME': config.get('storage', 'NAME'),
        'USER': config.get('storage', 'USER'),
        'PASSWORD': config.get('storage', 'PASSWORD'),
        'HOST': config.get('storage', 'HOST'),
        'PORT': config.get('storage', 'PORT'),
    }
}

#Use when testing out the creation and database setup
#DATABASES = {
#    'default': {
#        'ENGINE': config.get('teststorage', 'ENGINE'),
#       'NAME': config.get('teststorage', 'NAME'),
#        'USER': config.get('teststorage', 'USER'),
#        'PASSWORD': config.get('teststorage', 'PASSWORD'),
#        'HOST': config.get('teststorage', 'HOST'),
#        'PORT': config.get('teststorage', 'PORT'),
#    }
#}

CACHE_BACKEND = config.get('storage', 'CACHE_BACKEND')
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

CACHES = {
  'default': {
   'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
   'LOCATION': '127.0.0.1:11211',
  }
} 

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config.get('email', 'EMAIL_HOST')
EMAIL_PORT = config.get('email', 'EMAIL_PORT')
EMAIL_HOST_USER = config.get('email', 'EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config.get('email', 'EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config.get('email', 'EMAIL_USE_TLS')

NOREPLY_EMAIL = 'noreply@communityplanit.org'

# Localization
TIME_ZONE = config.get('localization', 'TIME_ZONE')
LANGUAGE_CODE = config.get('localization', 'LANGUAGE_CODE')
USE_I18N = config.getboolean('localization', 'USE_I18N') 
USE_L10N = config.getboolean('localization', 'USE_L10N')
LOCALE_PATHS = (
        os.path.join(ROOTDIR, '../locale'),
)

ugettext = lambda s: s
LANGUAGES = (
  ('ru', ugettext('Russian')),
  ('en', ugettext('English')),
  ('de', ugettext(u'Deutsch')),
  ('fr', ugettext(u'Français')),
)
#django-localeurl
LOCALE_INDEPENDENT_PATHS = (
    #re.compile('^/$'),
    re.compile('^/ajax/'),
    re.compile('^/assets/'),
    re.compile('^/admin-media/'),
    re.compile('^/favicon.ico$'),
)
LOCALE_INDEPENDENT_MEDIA_URL = config.getboolean('localeurl', 'LOCALE_INDEPENDENT_MEDIA_URL')
PREFIX_DEFAULT_LOCALE = config.getboolean('localeurl', 'PREFIX_DEFAULT_LOCALE')


# Media
MEDIA_ROOT = config.get('media', 'MEDIA_ROOT')
MEDIA_URL = '/assets/'
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Internal
TEMPLATE_DIRS = ( 'templates' )
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'localeurl.middleware.LocaleURLMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

# Application
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTHENTICATION_BACKENDS = ( 'web.accounts.backends.EmailBackend', )
ROOT_URLCONF = 'web.urls'
INSTALLED_APPS = (
    # localeurl should be first
    'localeurl',
    # Internal
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admindocs',
    'django.contrib.admin',

    # Applications
    'web.instances',
    'web.accounts',
    'web.reports',
    'web.missions',
    'web.games',
    'web.prompts',
    'web.responses',
    'web.attachments',
    'web.challenges',
    'web.comments',
    'web.values',
    'web.lists',
    'web.curator',
    'web.flags',
    'web.player_activities',
    'web.answers',
    'web.templatetags',

    # 3rd party
    'compressor',
    'south',
    'gmapsfield',
    'gmapsfield.templatetags',
    'nani',
    'django_extensions',
    'rosetta',
)

# Google maps settings
GMAP_JQUERY = config.get('gmaps', 'JQUERY')

# Default all to Boston
GMAP_DEFAULT = [42.355241376822725,-71.06010156250015]

# Default points/coins
DEFAULT_POINTS = 10
DEFAULT_COINS = 0

SERIALIZATION_MODULES = {
    'yaml': "django.core.serializers.pyyaml"

} 
