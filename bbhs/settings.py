import os

import ldap
from django_auth_ldap.config import LDAPSearch, ActiveDirectoryGroupType, LDAPSearchUnion

'''TODO
In eventPage.html
    + Change "if superuser" to "if in admin group"

Create user profile 

Phone number and department from LDAP in userprofile

Delete user form on chaperone page

URL Shortener

Implement {{ event.get_absolute_url }}/signup view+url

DJANGO LOGGING
Tech security group superuser access over LDAP
UNREGISTER FEATURE
'''

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Luis Naranjo', 'luisnaranjo733@gmail.com'),
)

MANAGERS = ADMINS

AUTH_PROFILE_MODULE = 'intranet.UserProfile'
LOGIN_URL = '/login/'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/user/%s/" % u.username,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/var/www/faculty.bishopblanchet.org/sqlite.db',
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'US/Pacific'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/www/faculty.bishopblanchet.org/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, 'static files'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n4=oo6dem%fjurp78xt=-@0g)atgo%u59ry+z&amp;pa94va*#_0v0'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bbhs.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bbhs.wsgi.application'

TEMPLATE_DIRS = (
        os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'intranet',
    'chaperone',
    'shortener',
    
    'clippy',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'stream_to_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django_auth_ldap': {
            'handlers': ['stream_to_console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# LDAP Auth config
# http://packages.python.org/django-auth-ldap/index.html
AUTHENTICATION_BACKENDS = (
 'django_auth_ldap.backend.LDAPBackend',
 'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP_SERVER_URI = "ldap://10.10.10.1"

AUTH_LDAP_BIND_DN  = 'CN=Luis Naranjo,OU=Technology,OU=Staff,DC=campus,DC=bishopblanchet,DC=org'
from passReader import AUTH_LDAP_BIND_PASSWORD

AUTH_LDAP_USER_SEARCH = LDAPSearch('ou=Staff,dc=campus,dc=bishopblanchet,dc=org', ldap.SCOPE_SUBTREE, '(sAMAccountName=%(user)s)')
# search for any user object under the Staff ou when authenticating
AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName", "last_name": "sn",
        'email': 'mail'}

faculty_cn = 'OU=Faculty,OU=Staff,DC=campus,DC=bishopblanchet,DC=org'
super_admin = 'cn=Intranet_Super_Admin,ou=Technology,ou=Staff,dc=campus,dc=bishopblanchet,dc=org'

AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {
    'isFaculty' : 'CN=intranet_faculty,' + faculty_cn
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    'is_superuser': super_admin,
    'is_staff': super_admin
}

AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType()

AUTH_LDAP_GROUP_SEARCH = LDAPSearch('ou=Staff,dc=campus,dc=bishopblanchet,dc=org',
        ldap.SCOPE_SUBTREE, '(cn=Staff)')


AUTH_LDAP_REQUIRE_GROUP = "cn=Staff,ou=staff,dc=campus,dc=bishopblanchet,dc=org"

AUTH_LDAP_MIRROR_GROUPS = True

# Use the security group only, don't rely on the OU

''' To do:
    Configure logging:
        - Django
        - Auth LDAP
        - Custom apps
'''

import logging

logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

DOMAIN = 'faculty.bishopblanchet.org'

username = 'bbhschaperone'
password = 'gobraves'
fromaddr = username+'@gmail.com'

from smtplib import SMTP, SMTPRecipientsRefused
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send(msg, toaddrs):
    if DEBUG:
        return
    server = SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    try:
        server.sendmail(fromaddr, [toaddrs], msg)
    except SMTPRecipientsRefused, tb:
        print 'Failed to email: ' + toaddrs
        print tb
    server.quit()

def sendTextEmail(msg, subject, toaddrs):
    msg = MIMEText(msg)
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['to'] = toaddrs
    send(msg.as_string(), toaddrs)
    
def sendHTMLEmail(text, html, subject, toaddrs):
    ''''Pass in alternative text and the intended html'''
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    send(msg.as_string(), toaddrs)

from datetime import datetime

endOfYear = datetime(2013, 7, 1)
startOfYear = datetime(2013, 9, 1)
