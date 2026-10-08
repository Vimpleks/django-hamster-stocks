from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery, Value, FloatField
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from threads.models import Project, ProjectThread, StockThread, BasketThread, Manufacturer, Thread
from threads.forms import ProjectForm, ThreadQuantityForm, ThreadUpdateProjectForm
from threads.services import get_quantity_color_in_storage, filter_by_field, add_thread_in_storage


@login_required
def projects(request):
    """
    Список проектов пользователя.
    """
    projects_user = Project.objects.filter(owner=request.user).order_by('name')

    filter_value = request.GET.get('name')
    projects_user = filter_by_field(projects_user, filter_value, 'name__icontains')

    return render(request, 'threads/projects.html', {
        'title': 'Запасы хомяка - Твои проекты',
        'projects': projects_user,
        'filter_value': filter_value,
    })


@login_required
def project_detail(request, project_id):
    """
    Детальная информация по проекту со списком ниток, который необходим для его вышивания.
    """
    project = get_object_or_404(Project, pk=project_id, owner=request.user)

    stock_subquery = StockThread.objects.filter(
        thread=OuterRef('thread'),
        stock__owner=request.user,
    ).values('quantity')

    basket_subquery = BasketThread.objects.filter(
        thread=OuterRef('thread'),
        basket__owner=request.user,
    ).values('quantity')

    project_threads = ProjectThread.objects.annotate(
        stock_quantity=Coalesce(Subquery(stock_subquery, output_field=FloatField()),
                                Value(0, output_field=FloatField())),
        basket_quantity=Coalesce(Subquery(basket_subquery, output_field=FloatField()),
                                 Value(0, output_field=FloatField()))
    ).select_related('thread__manufacturer').filter(project=project).order_by(
        'thread__manufacturer', 'thread__article')

    total_color = get_quantity_color_in_storage(project, ProjectThread, 'project')

    return render(request, 'threads/projects_detail.html', {
        'title': f'Запасы хомяка - {project.name}',
        'project': project,
        'project_threads': project_threads,
        'total_color': total_color,
    })


@login_required
def add_project(request):
    """
    Страница добавления нового проекта.
    """
    if request.method == 'POST':
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return HttpResponseRedirect(reverse('threads:projects'))
    else:
        form = ProjectForm()

    return render(request, 'threads/project_add.html', {
        'title': 'Запасы Хомяка - Создание проекта',
        'form': form,
    })


@login_required
def edit_project(request, project_id):
    """
    Страница изменения информации о проекте.
    """
    project = get_object_or_404(Project, pk=project_id, owner=request.user)

    if request.method == 'POST':
        form = ProjectForm(data=request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('threads:project_detail', args=[project_id]))
    else:
        form = ProjectForm(instance=project)

    return render(request, 'threads/project_edit.html', {
        'title': 'Запасы хомяка - Изменение проекта',
        'form': form,
        'project': project,
    })


@login_required
def delete_project(request, project_id):
    """
    Удаление проекта.
    """
    project = get_object_or_404(Project, pk=project_id, owner=request.user)

    if request.method == 'POST':
        project.delete()
        return redirect('threads:projects')

    return redirect('threads:projects')


@login_required
def add_thread_project(request, manufacturer_slug):
    """
    Страница добавления нитки в проект.
    """
    manufacturer = get_object_or_404(Manufacturer, slug=manufacturer_slug)
    threads = Thread.objects.select_related('manufacturer').filter(manufacturer=manufacturer).order_by('article')
    project_id = request.GET.get('project_id')

    if request.method == 'POST':
        form = ThreadQuantityForm(data=request.POST)
        if form.is_valid():
            thread_id = form.cleaned_data['thread']
            quantity = form.cleaned_data['quantity']
            project = get_object_or_404(Project, pk=project_id, owner=request.user)
            add_thread_in_storage(ProjectThread, quantity, thread_id, 'project', project)
            return HttpResponseRedirect(reverse('threads:project_detail', args=[project_id]))
    else:
        form = ThreadQuantityForm()

    return render(request, 'threads/threads_project_add.html', {
        'title': f'Запасы хомяка - Нитки {manufacturer}',
        'manufacturer': manufacturer,
        'threads': threads,
        'form': form,
        'project_id': project_id,
    })


@login_required
def update_thread_project(request, project_thread_id):
    """
    Страница изменения количества нитки в проекте.
    """
    project_thread = get_object_or_404(ProjectThread, pk=project_thread_id, project__owner=request.user)

    if request.method == 'POST':
        form = ThreadUpdateProjectForm(data=request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            project_thread.quantity = quantity
            project_thread.save(update_fields=['quantity'])
            return HttpResponseRedirect(reverse('threads:project_detail',
                                                args=[project_thread.project.id]))
    else:
        form = ThreadUpdateProjectForm()

    return render(request, 'threads/threads_project_update.html', {
        'title': f'Запасы хомяка - {project_thread.thread.manufacturer.name} {project_thread.thread.article}',
        'project_thread': project_thread,
        'form': form,
    })


@login_required
def delete_thread_project(request, project_thread_id):
    """
    Удаление нитки из проекта.
    """
    project_thread = get_object_or_404(ProjectThread, pk=project_thread_id, project__owner=request.user)

    if request.method == 'POST':
        project_thread.delete()
        return HttpResponseRedirect(reverse('threads:project_detail',
                                            args=[project_thread.project.id]))

    return redirect('threads:projects')
