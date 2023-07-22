import os
import warnings
from django.utils.translation import ugettext_lazy as _
from os.path import dirname

#warnings.simplefilter('error', DeprecationWarning)

BASE_DIR = dirname(dirname(dirname(dirname(os.path.abspath(__file__)))))
CONTENT_DIR = os.path.join(BASE_DIR, 'content')

SECRET_KEY = 'NhfTvayqggTBPswCXXhWaN69HuglgZIkM'

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1','54.184.183.101','echel.in']

SITE_ID = 1



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_crontab',
    #'rest_framework',

    # Vendor apps
    'hierarchy',
    'attendee',
    'common',
    
    'bootstrap4',
    'bootstrap_datepicker_plus',
    # Application apps
    'main',
    'accounts',
    
    
    'import_export',
    #'student',
    #'employee',
    'attendance',
    'leave',
]
BOOTSTRAP4 = {
    'include_jquery': True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(CONTENT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = os.path.join(CONTENT_DIR, 'tmp/emails')

EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_HOST_USER = 'AKIA6JBPADW4FRHKNPMM'
DEFAULT_FROM_EMAIL = 'contactus@radiantinfonet.com'
EMAIL_HOST_PASSWORD = 'BGIlWFRS0K+cKE/QJuMAWbNeFzNj6RSlGtkpe9R43Jrn'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testingdbhrms_2',
        'USER': 'root',
        'PASSWORD': 'root@123',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

CRONTAB_DJANGO_MANAGE_PATH = BASE_DIR + '/manage.py'
CRONTAB_DJANGO_PROJECT_NAME = BASE_DIR
CRONTAB_COMMAND_SUFFIX = '2>&1'

CRONJOBS = [
    #('0 0 1 * *','leave.cron.credit_leave_every_month','>> '+ BASE_DIR + '/file.log')
    ('* * * * *','leave.cron.credit_leave_every_month','>> '+ BASE_DIR + '/file.log')
    #('* * * * *','leave.cron.credit_leave_every_month')

]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ENABLE_USER_ACTIVATION = False
DISABLE_USERNAME = False
LOGIN_VIA_EMAIL = False
LOGIN_VIA_EMAIL_OR_USERNAME = True
LOGIN_REDIRECT_URL = 'accounts:dashboard_index'
LOGIN_URL = 'accounts:log_in'
USE_REMEMBER_ME = True
AUTH_USER_MODEL = 'accounts.User'
RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME = False
ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE = True

SIGN_UP_FIELDS = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
if DISABLE_USERNAME:
    SIGN_UP_FIELDS = ['first_name', 'last_name', 'email', 'password1', 'password2']

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('zh-Hans', _('Simplified Chinese')),
]

TIME_ZONE = 'UTC'
USE_TZ = True


LOGGING = {
'version': 1,
'disable_existing_loggers': False,
'handlers': {
    'file': {
        'level': 'INFO',
        'class': 'logging.FileHandler',
        'filename': 'debug.log',
    },
    'mail_admins': {
        'level': 'ERROR',
        'class': 'django.utils.log.AdminEmailHandler',
    },
},
'loggers': {
    'django': {
        'handlers': ['file'],
        'level': 'ERROR',
        'propagate': True,
    },
'main': {
        'handlers': ['file'],
        'level': 'INFO',
        'propagate': True,
    },
'accounts': {
        'handlers': ['file'],
        'level': 'INFO',
        'propagate': True,
    },
'common': {
        'handlers': ['file'],
        'level': 'INFO',
        'propagate': True,
    },
'hierarchy': {
        'handlers': ['file'],
        'level': 'INFO',
        'propagate': True,
    },
'attendee': {
        'handlers': ['file'],
        'level': 'INFO',
        'propagate': True,
    },
'student': {
        'handlers': ['file'],
        'level': 'INFO',
        'propagate': True,
    },
'employee': {
        'handlers': ['file'],
        'level': 'INFO',
        'propagate': True,
    },
'attendance': {
        'handlers': ['file'],
        'level': 'INFO',
        'propagate': True,
    },
'leave': {
        'handlers': ['file'],
        'level': 'INFO',
        'propagate': True,
    },
},
}

STATIC_ROOT = os.path.join(CONTENT_DIR, 'static')
DATA_ROOT1 = os.path.join(BASE_DIR, 'static')
DATA_ROOT = os.path.join(DATA_ROOT1, 'data')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(CONTENT_DIR, 'media')
MEDIA_URL = '/media/'
JUNK_ROOT = os.path.join(MEDIA_ROOT, 'junk')
JUNK_URL = '/junk/'

STATICFILES_DIRS = [
    os.path.join(CONTENT_DIR, 'assets'),
]

LOCALE_PATHS = [
    os.path.join(CONTENT_DIR, 'locale')
]
CLIENT_SALT='Q@F$5GBdd2ty$#F*fn2u4'
CLIENT_KEY='thisisfortesting'

AWS_ACCESS_KEY_ID = 'AKIA6JBPADW4DLWMOJBN'
AWS_SECRET_ACCESS_KEY = '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'
