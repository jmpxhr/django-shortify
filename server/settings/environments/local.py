from typing import Any

from server.settings.components import BASE_DIR

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES: dict[str, dict[str, Any]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}
