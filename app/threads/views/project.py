from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery, Value, FloatField
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from threads.models import Project, ProjectThread, StockThread, BasketThread, Manufacturer, Thread
from threads.forms import ProjectForm, ThreadQuantityForm, ThreadUpdateProjectForm


@login_required
def projects(request):
    projects_user = Project.objects.filter(owner=request.user)

    filter_article = request.GET.get('name')
    if filter_article:
        projects_user = projects_user.filter(name__icontains=filter_article)

    context = {
        'title': 'Запасы хомяка - Твои проекты',
        'projects': projects_user
    }
    return render(request, 'threads/projects.html', context)


@login_required
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)

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

    total_color = project.total_color()

    context = {
        'title': f'Запасы хомяка - {project.name}',
        'project': project,
        'project_threads': project_threads,
        'total_color': total_color,
    }
    return render(request, 'threads/projects_detail.html', context)


@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('threads:projects'))
    else:
        form = ProjectForm()

    context = {
        'title': 'Запасы Хомяка - Создание проекта',
        'form': form,
    }

    return render(request, 'threads/project_add.html', context)


@login_required()
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(data=request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('threads:project_detail', args=[project_id]))
    else:
        form = ProjectForm(instance=project)

    context = {
        'title': 'Запасы хомяка - Изменение проекта',
        'form': form,
        'project': project,
    }
    return render(request, 'threads/project_edit.html', context)


@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('threads:projects')

    return redirect('threads:projects')


@login_required
def manufacturers_project(request):
    manufacturers = Manufacturer.objects.all()
    project = request.GET.get('project_id')
    return render(request, 'threads/manufacturers_project.html', {
        'title': 'Запасы хомяка - Производители',
        'manufacturers': manufacturers,
        'project': project
    })


@login_required
def add_thread_project(request, manufacturer_slug):
    manufacturer = Manufacturer.objects.get(slug=manufacturer_slug)
    threads = Thread.objects.select_related('manufacturer').filter(manufacturer=manufacturer).order_by('article')
    project_id = request.GET.get('project_id')

    filter_article = request.GET.get('article')
    if filter_article:
        threads = threads.filter(article__icontains=filter_article)

    if request.method == 'POST':
        form = ThreadQuantityForm(data=request.POST)
        if form.is_valid():
            thread_id = form.cleaned_data['thread']
            quantity = abs(form.cleaned_data['quantity'])
            project = Project.objects.get(id=project_id)
            try:
                project_stock = ProjectThread.objects.get(project=project, thread=thread_id)
                quantity_add = project_stock.quantity + quantity
                project_stock.quantity = quantity_add
                project_stock.save(update_fields=['quantity'])
            except ProjectThread.DoesNotExist:
                thread = Thread.objects.get(id=thread_id)
                ProjectThread.objects.create(project=project, thread=thread, quantity=quantity)
            return HttpResponseRedirect(reverse('threads:project_detail', args=[project_id]))
    else:
        form = ThreadQuantityForm()

    context = {
        'title': f'Запасы хомяка - Нитки {manufacturer}',
        'manufacturer': manufacturer,
        'threads': threads,
        'form': form,
        'article': filter_article,
        'project_id': project_id,
    }
    return render(request, 'threads/threads_project_add.html', context)


@login_required
def update_thread_project(request, project_thread_id):
    project_thread = get_object_or_404(ProjectThread, pk=project_thread_id)
    if request.method == 'POST':
        form = ThreadUpdateProjectForm(data=request.POST)
        if form.is_valid():
            quantity = abs(form.cleaned_data['quantity'])
            project_thread.quantity = quantity
            project_thread.save(update_fields=['quantity'])

            return HttpResponseRedirect(reverse('threads:project_detail', args=[project_thread.project.id]))
    else:
        form = ThreadUpdateProjectForm()

    context = {
        'title': f'Запасы хомяка - {project_thread.thread.manufacturer.name} {project_thread.thread.article}',
        'project_thread': project_thread,
        'form': form,
    }
    return render(request, 'threads/threads_project_update.html', context)


@login_required
def delete_thread_project(request, project_thread_id):
    project_thread = get_object_or_404(ProjectThread, pk=project_thread_id)
    if request.method == 'POST':
        project_thread.delete()
        return HttpResponseRedirect(reverse('threads:project_detail', args=[project_thread.project.id]))

    return redirect('threads:projects')
