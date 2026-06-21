from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from threads.models import Basket, BasketThread, Manufacturer, Thread
from threads.forms import ThreadQuantityForm, ThreadUpdateBasketForm


@login_required
def basket(request):
    basket_user = Basket.objects.get(owner=request.user)
    basket_threads = BasketThread.objects.select_related('thread__manufacturer').filter(basket=basket_user).order_by('thread__manufacturer', 'thread__article')

    total_color = basket_user.total_color()
    total_quantity = basket_user.total_quantity()

    filter_article = request.GET.get('article')
    if filter_article:
        basket_threads = basket_threads.filter(thread__article__icontains=filter_article)

    return render(request, 'threads/basket.html', context={
        'title': 'Запасы хомяка - Список покупок',
        'basket_threads': basket_threads,
        'total_color': total_color,
        'total_quantity': total_quantity,
        'article': filter_article,
    })


@login_required
def manufacturers_basket(request):
    manufacturers = Manufacturer.objects.all()
    return render(request, 'threads/manufacturers_basket.html', {
        'title': 'Запасы хомяка - Производители',
        'manufacturers': manufacturers
    })


@login_required
def thread_basket_add(request, manufacturer_slug):
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
            basket_user = Basket.objects.get(owner=request.user)
            try:
                thread_basket = BasketThread.objects.get(basket=basket_user, thread=thread_id)
                quantity_add = thread_basket.quantity + quantity
                thread_basket.quantity = quantity_add
                thread_basket.save(update_fields=['quantity'])
            except BasketThread.DoesNotExist:
                thread = Thread.objects.get(id=thread_id)
                BasketThread.objects.create(basket=basket_user, thread=thread, quantity=quantity)
            return HttpResponseRedirect(reverse('threads:basket'))
    else:
        form = ThreadQuantityForm()

    context = {
        'title': f'Запасы хомяка - Нитки {manufacturer}',
        'manufacturer': manufacturer,
        'threads': threads,
        'form': form,
        'article': filter_article,
    }
    return render(request, 'threads/threads_basket_add.html', context)


@login_required
def thread_basket_update(request, basket_thread_id):
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

    context = {
        'title': f'Запасы хомяка - {basket_thread.thread.manufacturer.name} {basket_thread.thread.article}',
        'basket_thread': basket_thread,
        'form': form,
    }
    return render(request, 'threads/threads_basket_update.html', context)
#
#
@login_required
def thread_basket_delete(request, basket_thread_id):
    basket_thread = get_object_or_404(BasketThread, pk=basket_thread_id)
    if request.method == 'POST':
        basket_thread.delete()
        # messages.success(request, 'Книга успешно удалена.')
        # Редирект на ту же страницу (список книг)
        return redirect('threads:basket')

        # Если кто-то зашёл на URL через GET — просто показываем список
    return redirect('threads:basket')