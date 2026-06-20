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
    path('manufacturers/<slug:manufacturer_slug>/', views.manufacturer_detail, name='manufacturer_detail'),
    path('stock/', views.stock, name='stock'),
    path('stock/manufacturers/', views.manufacturers_stock, name='manufacturers_stock'),
    path('stock/manufacturers/<slug:manufacturer_slug>/', views.thread_stock_add, name='thread_add_stock'),
    path('stock/<int:stock_thread_id>/update/', views.thread_stock_update, name='thread_stock_update'),
    path('stock/<int:stock_thread_id>/delete/', views.thread_stock_delete, name='thread_stock_delete'),
]
