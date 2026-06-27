from .base import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # указать реальный домен при деплое

# SECRET_KEY должен быть задан через переменную окружения:
# export DJANGO_SECRET_KEY='...'
# import os
# SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
