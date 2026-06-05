from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from users.forms import UserLoginForm, UserRegistrationForm

from threads.models import Stock, Basket


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('threads:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Запасы Хомяка - Авторизация',
        'form': form,
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            Stock.objects.create(owner=user)
            Basket.objects.create(owner=user)
            auth.login(request, user)
            return HttpResponseRedirect(reverse('threads:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Запасы Хомяка - Регистрация',
        'form': form,
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):
    context = {
        'title': 'Запасы Хомяка - Мой профиль',
    }
    return render(request, 'users/profile.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('threads:index'))
