from django.contrib import admin
from threads.models import Manufacturers, Threads


@admin.register(Manufacturers)
class ManufacturersAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(Threads)
class ThreadsAdmin(admin.ModelAdmin):
    list_display = ['article', 'name', 'manufacturer']
    search_fields = ['article', 'name']
