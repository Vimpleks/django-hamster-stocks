from django.shortcuts import render

from threads.models import Manufacturer, Thread


def manufacturer(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'threads/manufacturers.html', {
        'title': 'Запасы хомяка - Производители',
        'manufacturers': manufacturers,
    })


def manufacturer_detail(request, manufacturer_slug):
    manufacturer = Manufacturer.objects.get(slug=manufacturer_slug)
    threads = Thread.objects.select_related('manufacturer').filter(manufacturer=manufacturer).order_by('article')
    filter_article = request.GET.get('article')
    if filter_article:
        threads = threads.filter(article__icontains=filter_article)
    return render(request, 'threads/threads.html', {
        'title': f'Запасы хомяка - Нитки {manufacturer.name}',
        'manufacturer': manufacturer,
        'threads': threads,
        'article': filter_article,
    })
