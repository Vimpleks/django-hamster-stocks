"""
URL-маршруты приложения threads.

Каждая строка связывает URL-путь с функцией-view.
"""

from django.urls import path
from threads import views

app_name = 'threads'

urlpatterns = [
    path('', views.index, name='index'),
    path('manufacturers/', views.manufacturer, name='manufacturers'),
]
