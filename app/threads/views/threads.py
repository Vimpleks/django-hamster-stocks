from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from threads.models import Manufacturer, Thread, StockThread, BasketThread, ProjectThread


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

    context = {
        'title': f'Запасы хомяка - Нитки {manufacturer.name}',
        'manufacturer': manufacturer,
        'threads': threads,
        'article': filter_article,
    }

    return render(request, 'threads/threads.html', context)


@login_required
def thread_detail(request, thread_id):
    thread = Thread.objects.get(id=thread_id)

    stock_thread = StockThread.objects.filter(id=thread_id, stock__owner=request.user)
    stock_count = stock_thread[0].quantity if stock_thread else 0

    basket_thread = BasketThread.objects.filter(id=thread_id, basket__owner=request.user)
    basket_count = basket_thread[0].quantity if basket_thread else 0

    project_threads = ProjectThread.objects.filter(thread=thread, project__owner=request.user)

    context = {
        'title': f'Запасы хомяка - {thread.manufacturer.name} {thread.article}',
        'thread': thread,
        'stock_count': stock_count,
        'basket_count': basket_count,
        'project_threads': project_threads,
    }

    return render(request, 'threads/thread_detail.html', context)
