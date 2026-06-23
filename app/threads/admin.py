from django.contrib import admin
from threads.models import Manufacturer, Thread, Stock, StockThread, Project, ProjectThread, Basket, BasketThread


@admin.register(Manufacturer)
class ManufacturersAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Thread)
class ThreadsAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'name', 'manufacturer']
    search_fields = ['article', 'name']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner']


@admin.register(StockThread)
class StockThreadAdmin(admin.ModelAdmin):
    list_display = ['id', 'stock', 'thread', 'quantity']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner']


@admin.register(ProjectThread)
class ProjectThreadAdmin(admin.ModelAdmin):
    list_display = ['project', 'thread']


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner']


@admin.register(BasketThread)
class BasketThreadAdmin(admin.ModelAdmin):
    list_display = ['basket', 'thread']
