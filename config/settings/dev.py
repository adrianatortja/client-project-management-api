from .base import *  # noqa: F401,F403
from .base import env

DEBUG = True

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

CORS_ALLOWED_ORIGINS = env.list(
    'CORS_ALLOWED_ORIGINS', default=['http://localhost:5173']
)
