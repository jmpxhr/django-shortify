import logging
import socket

from server.settings.components import config
from server.settings.components.common import (
    DATABASES,
    INSTALLED_APPS,
    MIDDLEWARE,
)
from server.settings.components.cors import CORS_ALLOWED_ORIGINS

# Setting the development status:

DEBUG = True

ALLOWED_HOSTS: list[str] = [
    config('DOMAIN_NAME'),
    'localhost',
    '0.0.0.0',  # noqa: S104
    '127.0.0.1',
    '[::1]',
]

# Installed apps for development only:

INSTALLED_APPS += (
    # Better debug:
    'debug_toolbar',
    'zeal',
)

# Django debug toolbar:
# https://django-debug-toolbar.readthedocs.io

MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
try:  # This might fail on some OS
    INTERNAL_IPS = [
        '{}.1'.format(ip[: ip.rfind('.')])
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    ]
except OSError:  # pragma: no cover
    INTERNAL_IPS = []
INTERNAL_IPS += ['127.0.0.1', '10.0.2.2']

# django-cors-headers

CORS_ALLOWED_ORIGINS.extend([
    'http://localhost',
    'http://127.0.0.1',
])

# django-zeal
# https://github.com/taobojlen/django-zeal

# Should be the first in line:
MIDDLEWARE = ('zeal.middleware.zeal_middleware', *MIDDLEWARE)

# Logging N+1 requests:
ZEAL_RAISE = True  # comment out if you want to allow N+1 requests
ZEAL_SHOW_ALL_CALLERS = True
ZEAL_LOGGER = logging.getLogger('django')
ZEAL_ALLOWLIST = [
    {'model': 'admin.*'},
]

# Disable persistent DB connections
# https://docs.djangoproject.com/en/6.0/ref/databases/#caveats
DATABASES['default']['CONN_MAX_AGE'] = 0
