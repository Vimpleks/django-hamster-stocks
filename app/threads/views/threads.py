from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from threads.models import Manufacturer, Thread, StockThread, BasketThread, ProjectThread
from threads.services import filter_by_field


def manufacturer(request):
    manufacturers = Manufacturer.objects.all()
    source = request.GET.get('source', 'index')
    project = request.GET.get('project_id')
    return render(request, 'threads/manufacturers.html', {
        'title': 'Запасы хомяка - Производители',
        'manufacturers': manufacturers,
        'source': source,
        'project': project,
    })


def manufacturer_detail(request, manufacturer_slug):
    manufacturer = Manufacturer.objects.get(slug=manufacturer_slug)
    threads = Thread.objects.select_related('manufacturer').filter(manufacturer=manufacturer).order_by('article')

    filter_value = request.GET.get('article')
    threads = filter_by_field(threads, filter_value, 'article__icontains')

    return render(request, 'threads/threads.html', {
        'title': f'Запасы хомяка - Нитки {manufacturer.name}',
        'manufacturer': manufacturer,
        'threads': threads,
        'filter_value': filter_value,
    })


@login_required
def thread_detail(request, thread_id):
    thread = Thread.objects.get(id=thread_id)

    stock_thread = StockThread.objects.filter(id=thread_id, stock__owner=request.user)
    stock_count = stock_thread[0].quantity if stock_thread else 0

    basket_thread = BasketThread.objects.filter(id=thread_id, basket__owner=request.user)
    basket_count = basket_thread[0].quantity if basket_thread else 0

    project_threads = ProjectThread.objects.filter(thread=thread, project__owner=request.user)

    return render(request, 'threads/thread_detail.html', {
        'title': f'Запасы хомяка - {thread.manufacturer.name} {thread.article}',
        'thread': thread,
        'stock_count': stock_count,
        'basket_count': basket_count,
        'project_threads': project_threads,
    })
