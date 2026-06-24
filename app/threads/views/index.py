from django.shortcuts import render


def index(request):
    """
    Главная страница.
    """
    return render(request, "threads/index.html", context={
        'title': 'Запасы хомяка'
    })
