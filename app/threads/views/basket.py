from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from threads.models import Basket, BasketThread, Manufacturer, Thread
from threads.forms import ThreadQuantityForm, ThreadUpdateBasketForm
from threads.services import get_quantity_thread_in_storage, get_quantity_color_in_storage, filter_by_field, \
    add_thread_in_storage


@login_required
def basket(request):
    """
    Страница списка покупок (корзины) со списком, хранящихся в ней ниток.
    """
    basket_user = Basket.objects.get(owner=request.user)
    basket_threads = BasketThread.objects.select_related('thread__manufacturer').filter(basket=basket_user).order_by(
        'thread__manufacturer', 'thread__article')

    total_color = get_quantity_color_in_storage(basket_user, BasketThread, 'basket')
    total_quantity = get_quantity_thread_in_storage(basket_user, BasketThread, 'basket')

    filter_value = request.GET.get('article')
    basket_threads = filter_by_field(basket_threads, filter_value, 'thread__article__icontains')

    return render(request, 'threads/basket.html', {
        'title': 'Запасы хомяка - Список покупок',
        'basket_threads': basket_threads,
        'total_color': total_color,
        'total_quantity': total_quantity,
        'filter_value': filter_value,
    })


@login_required
def add_thread_basket(request, manufacturer_slug):
    """
    Страница добавления нитки в корзину.
    """
    manufacturer = Manufacturer.objects.get(slug=manufacturer_slug)
    threads = Thread.objects.select_related('manufacturer').filter(manufacturer=manufacturer).order_by('article')

    filter_value = request.GET.get('article')
    threads = filter_by_field(threads, filter_value, 'article__icontains')

    if request.method == 'POST':
        form = ThreadQuantityForm(data=request.POST)
        if form.is_valid():
            thread_id = form.cleaned_data['thread']
            quantity = abs(form.cleaned_data['quantity'])
            basket_user = Basket.objects.get(owner=request.user)
            add_thread_in_storage(BasketThread, quantity, thread_id, 'basket', basket_user)
            return HttpResponseRedirect(reverse('threads:basket'))
    else:
        form = ThreadQuantityForm()

    return render(request, 'threads/threads_basket_add.html', {
        'title': f'Запасы хомяка - Нитки {manufacturer}',
        'manufacturer': manufacturer,
        'threads': threads,
        'form': form,
        'filter_value': filter_value,
    })


@login_required
def update_thread_basket(request, basket_thread_id):
    """
    Страница изменения количества нитки в корзине.
    """
    basket_thread = get_object_or_404(BasketThread, pk=basket_thread_id)

    if request.method == 'POST':
        form = ThreadUpdateBasketForm(data=request.POST)
        if form.is_valid():
            quantity = abs(form.cleaned_data['quantity'])
            basket_thread.quantity = quantity
            basket_thread.save(update_fields=['quantity'])
            return HttpResponseRedirect(reverse('threads:basket'))
    else:
        form = ThreadUpdateBasketForm()

    return render(request, 'threads/threads_basket_update.html', {
        'title': f'Запасы хомяка - {basket_thread.thread.manufacturer.name} {basket_thread.thread.article}',
        'basket_thread': basket_thread,
        'form': form,
    })


@login_required
def delete_thread_basket(request, basket_thread_id):
    """
    Удаление нитки из корзины.
    """
    basket_thread = get_object_or_404(BasketThread, pk=basket_thread_id)

    if request.method == 'POST':
        basket_thread.delete()
        return redirect('threads:basket')

    return redirect('threads:basket')
