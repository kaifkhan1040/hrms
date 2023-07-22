import os

IS_PRODUCTION = os.environ.get('IS_PRODUCTION')

try:
    from collections.abc import Callable
except ImportError:
    from collections import Callable

if IS_PRODUCTION:
    from .conf.production.settings import *
else:
    from .conf.development.settings import *

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

LOGIN_URL = '/accounts/log-in/'
#MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

