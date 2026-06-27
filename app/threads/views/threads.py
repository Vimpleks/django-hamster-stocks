from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from threads.models import Manufacturer, Thread, StockThread, BasketThread, ProjectThread
from threads.services import filter_by_field


def manufacturer(request):
    """
    Страница со списком производителей ниток.
    """
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
    """
    Список ниток выбранного производителя.
    """
    manufacturer = get_object_or_404(Manufacturer, slug=manufacturer_slug)
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
    """
    Детальная информация о нитке.
    Количество ее в запасах и списке покупок (корзине).
    Проекты, в которых необходима эта нитка, с количеством.
    """
    thread = get_object_or_404(Thread, id=thread_id)

    stock_thread = StockThread.objects.filter(thread=thread, stock__owner=request.user).first()
    stock_count = stock_thread.quantity if stock_thread else 0

    basket_thread = BasketThread.objects.filter(thread=thread, basket__owner=request.user).first()
    basket_count = basket_thread.quantity if basket_thread else 0

    project_threads = ProjectThread.objects.filter(thread=thread, project__owner=request.user)

    return render(request, 'threads/thread_detail.html', {
        'title': f'Запасы хомяка - {thread.manufacturer.name} {thread.article}',
        'thread': thread,
        'stock_count': stock_count,
        'basket_count': basket_count,
        'project_threads': project_threads,
    })
