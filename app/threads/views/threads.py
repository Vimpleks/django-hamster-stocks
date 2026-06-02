from django.shortcuts import render
from threads.models import Manufacturer


def manufacturer(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'threads/manufacturers.html', {
        'manufacturers': manufacturers
    })
