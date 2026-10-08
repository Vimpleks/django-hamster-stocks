from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from threads.models import Stock, StockThread, Manufacturer, Thread
from threads.forms import ThreadQuantityForm, ThreadUpdateStockForm
from threads.services import get_quantity_thread_in_storage, get_quantity_color_in_storage, filter_by_field, \
    add_thread_in_storage


@login_required
def stock(request):
    """
    Страница коробки с нитками (запаса) со списком, хранящихся в ней ниток.
    """
    stock_user = get_object_or_404(Stock, owner=request.user)
    stock_threads = StockThread.objects.select_related('thread__manufacturer').filter(stock=stock_user).order_by(
        'thread__manufacturer', 'thread__article')

    total_color = get_quantity_color_in_storage(stock_user, StockThread, 'stock')
    total_quantity = get_quantity_thread_in_storage(stock_user, StockThread, 'stock')

    filter_value = request.GET.get('article')
    stock_threads = filter_by_field(stock_threads, filter_value, 'thread__article__icontains')

    return render(request, 'threads/stock.html', {
        'title': 'Запасы хомяка - Твои запасы',
        'stock_threads': stock_threads,
        'total_color': total_color,
        'total_quantity': total_quantity,
        'filter_value': filter_value,
    })


@login_required
def add_thread_stock(request, manufacturer_slug):
    """
    Страница добавления нитки в запас.
    """
    manufacturer = get_object_or_404(Manufacturer, slug=manufacturer_slug)
    threads = Thread.objects.select_related('manufacturer').filter(manufacturer=manufacturer).order_by('article')

    filter_value = request.GET.get('article')
    threads = filter_by_field(threads, filter_value, 'article__icontains')

    if request.method == 'POST':
        form = ThreadQuantityForm(data=request.POST)
        if form.is_valid():
            thread_id = form.cleaned_data['thread']
            quantity = form.cleaned_data['quantity']
            stock_user = Stock.objects.get(owner=request.user)
            add_thread_in_storage(StockThread, quantity, thread_id, 'stock', stock_user)
            return HttpResponseRedirect(reverse('threads:stock'))
    else:
        form = ThreadQuantityForm()

    return render(request, 'threads/threads_stock_add.html', {
        'title': f'Запасы хомяка - Нитки {manufacturer}',
        'manufacturer': manufacturer,
        'threads': threads,
        'form': form,
        'filter_value': filter_value,
    })


@login_required
def update_thread_stock(request, stock_thread_id):
    """
    Страница изменения количества нитки в запасе.
    """
    stock_thread = get_object_or_404(StockThread, pk=stock_thread_id, stock__owner=request.user)

    if request.method == 'POST':
        form = ThreadUpdateStockForm(data=request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            stock_thread.quantity = quantity
            stock_thread.save(update_fields=['quantity'])
            return HttpResponseRedirect(reverse('threads:stock'))
    else:
        form = ThreadUpdateStockForm()

    return render(request, 'threads/threads_stock_update.html', {
        'title': f'Запасы хомяка - {stock_thread.thread.manufacturer.name} {stock_thread.thread.article}',
        'stock_thread': stock_thread,
        'form': form,
    })


@login_required
def delete_thread_stock(request, stock_thread_id):
    """
    Удаление нитки из запаса.
    """
    stock_thread = get_object_or_404(StockThread, pk=stock_thread_id, stock__owner=request.user)

    if request.method == 'POST':
        stock_thread.delete()
        return redirect('threads:stock')

    return redirect('threads:stock')
