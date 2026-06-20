from django.shortcuts import render

from threads.models import Manufacturer, Thread


def manufacturer(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'threads/manufacturers.html', {
        'manufacturers': manufacturers
    })


def manufacturer_detail(request, manufacturer_slug):
    manufacturer = Manufacturer.objects.get(slug=manufacturer_slug)
    threads = Thread.objects.filter(manufacturer=manufacturer).order_by('article')
    return render(request, 'threads/threads.html', {
        'manufacturer': manufacturer,
        'threads': threads
    })
