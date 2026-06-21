from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from threads.models import Stock, StockThread, Manufacturer, Thread
from threads.forms import ThreadQuantityForm, ThreadUpdateStockForm


@login_required
def stock(request):
    stock_user = Stock.objects.get(owner=request.user)
    stock_threads = StockThread.objects.select_related('thread__manufacturer').filter(stock=stock_user).order_by('thread__manufacturer', 'thread__article')

    total_color = stock_user.total_color()
    total_quantity = stock_user.total_quantity()

    filter_article = request.GET.get('article')
    if filter_article:
        stock_threads = stock_threads.filter(thread__article__icontains=filter_article)

    return render(request, 'threads/stock.html', context={
        'title': 'Запасы хомяка - Твои запасы',
        'stock_threads': stock_threads,
        'total_color': total_color,
        'total_quantity': total_quantity,
        'article': filter_article,
    })


@login_required
def manufacturers_stock(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'threads/manufacturers_stock.html', {
        'title': 'Запасы хомяка - Производители',
        'manufacturers': manufacturers
    })


@login_required
def thread_stock_add(request, manufacturer_slug):
    manufacturer = Manufacturer.objects.get(slug=manufacturer_slug)
    threads = Thread.objects.select_related('manufacturer').filter(manufacturer=manufacturer).order_by('article')

    filter_article = request.GET.get('article')
    if filter_article:
        threads = threads.filter(article__icontains=filter_article)

    if request.method == 'POST':
        form = ThreadQuantityForm(data=request.POST)
        if form.is_valid():
            thread_id = form.cleaned_data['thread']
            quantity = abs(form.cleaned_data['quantity'])
            stock_user = Stock.objects.get(owner=request.user)
            try:
                thread_stock = StockThread.objects.get(stock=stock_user, thread=thread_id)
                quantity_add = thread_stock.quantity + quantity
                thread_stock.quantity = quantity_add
                thread_stock.save(update_fields=['quantity'])
            except StockThread.DoesNotExist:
                thread = Thread.objects.get(id=thread_id)
                StockThread.objects.create(stock=stock_user, thread=thread, quantity=quantity)
            return HttpResponseRedirect(reverse('threads:stock'))
    else:
        form = ThreadQuantityForm()

    context = {
        'title': f'Запасы хомяка - Нитки {manufacturer}',
        'manufacturer': manufacturer,
        'threads': threads,
        'form': form,
        'article': filter_article,
    }
    return render(request, 'threads/threads_stock_add.html', context)


@login_required
def thread_stock_update(request, stock_thread_id):
    stock_thread = get_object_or_404(StockThread, pk=stock_thread_id)
    if request.method == 'POST':
        form = ThreadUpdateStockForm(data=request.POST)
        if form.is_valid():
            quantity = abs(form.cleaned_data['quantity'])
            stock_thread.quantity = quantity
            stock_thread.save(update_fields=['quantity'])

            return HttpResponseRedirect(reverse('threads:stock'))
    else:
        form = ThreadUpdateStockForm()

    context = {
        'title': f'Запасы хомяка - {stock_thread.thread.manufacturer.name} {stock_thread.thread.article}',
        'stock_thread': stock_thread,
        'form': form,
    }
    return render(request, 'threads/threads_stock_update.html', context)


@login_required
def thread_stock_delete(request, stock_thread_id):
    stock_thread = get_object_or_404(StockThread, pk=stock_thread_id)
    if request.method == 'POST':
        stock_thread.delete()
        # messages.success(request, 'Книга успешно удалена.')
        # Редирект на ту же страницу (список книг)
        return redirect('threads:stock')

        # Если кто-то зашёл на URL через GET — просто показываем список
    return redirect('threads:stock')
