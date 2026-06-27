from django.urls import reverse

from threads.forms import ThreadQuantityForm, ThreadUpdateProjectForm, ProjectForm
from threads.models import ProjectThread, Project


def test_projects_authenticated_user(logged_in_client, project):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:projects'))

    # Assert
    assert response.status_code == 200
    assert response.context['title'] == 'Запасы хомяка - Твои проекты'
    assert list(response.context['projects']) == [project]
    assert response.context['filter_value'] is None


def test_projects_unauthenticated_redirects(client):
    # Act
    response = client.get(reverse('threads:projects'), follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_projects_filters_by_name(logged_in_client, project, user):
    # Arrange
    client, user = logged_in_client
    Project.objects.create(
        name='Утро Нового года',
        status='kitted',
        owner=user,
    )

    # Act
    response = client.get(reverse('threads:projects'), {'name': 'доми'})

    # Assert
    assert response.status_code == 200
    assert response.context['projects'].count() == 1
    assert response.context['projects'].first().name == 'Акварельные домики'
    assert response.context['filter_value'] == 'доми'


def test_project_detail_authenticated_user(logged_in_client, project, first_project_thread, first_stock_thread,
                                           first_basket_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:project_detail', kwargs={'project_id': project.id}))

    # Assert
    assert response.status_code == 200
    assert response.context['title'].startswith('Запасы хомяка - ')
    assert list(response.context['project_threads']) == [first_project_thread]
    assert response.context['project_threads'].first().stock_quantity == 1
    assert response.context['project_threads'].first().basket_quantity == 1


def test_project_detail_unauthenticated_redirects(client, project):
    # Act
    response = client.get(reverse('threads:project_detail', kwargs={'project_id': project.id}),
                          follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_project_detail_invalid_project_id_returns_404(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:project_detail',
                                  kwargs={'project_id': 123}))

    # Assert
    assert response.status_code == 404


def test_project_detail_annotations_default_to_zero(logged_in_client, project, first_project_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:project_detail', kwargs={'project_id': project.id}))

    # Assert
    assert response.status_code == 200
    assert response.context['project_threads'].count() == 1
    assert response.context['project_threads'].first().stock_quantity == 0
    assert response.context['project_threads'].first().basket_quantity == 0


def test_add_project_authenticated_user(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:add_project'))

    # Assert
    assert response.status_code == 200
    assert isinstance(response.context['form'], ProjectForm)
    assert response.context['title'] == 'Запасы Хомяка - Создание проекта'


def test_add_project_unauthenticated_redirects(client):
    # Act
    response = client.get(reverse('threads:add_project'), follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_add_project_post_success(logged_in_client, user):
    # Arrange
    client, user = logged_in_client
    data = {
        'name': 'Акварельные домики',
        'description': 'Похожи на норвежские домики',
        'designer': 'Наталья Юркевич',
        'status': 'kitted',
        'owner': user.id,
    }

    # Act
    response = client.post(reverse('threads:add_project'), data=data, follow=False)

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:projects') in response.url
    assert Project.objects.filter(
        name='Акварельные домики',
        owner=user,
    ).exists()


def test_edit_project_authenticated_user(logged_in_client, project):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:edit_project',
                                  kwargs={'project_id': project.id}))

    # Assert
    assert response.status_code == 200
    assert response.context['form'].initial['name'] == project.name
    assert response.context['form'].initial['description'] == project.description
    assert response.context['form'].initial['designer'] == project.designer
    assert response.context['form'].initial['status'] == project.status
    assert response.context['project'] == project
    assert response.context['title'] == 'Запасы хомяка - Изменение проекта'


def test_edit_project_post_successfully_updates(logged_in_client, user, project):
    # Arrange
    client, user = logged_in_client
    data = {
        'name': 'Домики',
        'status': 'complete',
        'owner': user.id,
    }

    # Act
    response = client.post(reverse('threads:edit_project',
                                   kwargs={'project_id': project.id}), data)

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:project_detail', args=[str(project.id)]) in response.url
    assert Project.objects.filter(
        id=project.id,
        name='Домики',
        status='complete',
        owner=user,
    ).exists()


def test_edit_project_unauthenticated_redirects(client, project):
    # Act
    response = client.get(reverse('threads:edit_project',
                                  kwargs={'project_id': project.id}))

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_edit_project_invalid_project_id_returns_404(logged_in_client, user):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:edit_project',
                                  kwargs={'project_id': 123}))

    # Assert
    assert response.status_code == 404


def test_delete_project_post_success_delete(logged_in_client, project):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.post(reverse('threads:delete_project', kwargs={'project_id': project.id}))

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:projects') in response.url
    assert not Project.objects.filter(id=project.id).exists()


def test_delete_project_get_does_not_delete(logged_in_client, project):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:delete_project', kwargs={'project_id': project.id}))

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:projects') in response.url
    assert Project.objects.filter(id=project.id).exists()


def test_delete_project_unauthenticated_redirects(client):
    # Act
    response = client.get(reverse('threads:delete_project', kwargs={'project_id': 123}),
                          follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_delete_project_invalid_project_id_returns_404(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:delete_project', kwargs={'project_id': 123}))

    # Assert
    assert response.status_code == 404


def test_add_thread_project_authenticated_user(logged_in_client, manufacturer, first_thread, project):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:add_thread_project',
                                  kwargs={'manufacturer_slug': manufacturer.slug}), {'project_id': '123'})

    # Assert
    assert response.status_code == 200
    assert response.context['title'].startswith('Запасы хомяка - Нитки')
    assert response.context['manufacturer'] == manufacturer
    assert list(response.context['threads']) == [first_thread]
    assert response.context['project_id'] == '123'
    assert isinstance(response.context['form'], ThreadQuantityForm)


def test_add_thread_project_unauthenticated_redirects(client, manufacturer):
    # Act
    response = client.get(reverse('threads:add_thread_project',
                                  kwargs={'manufacturer_slug': manufacturer.slug}),
                          {'project_id': '123'}, follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_add_thread_project_post_success(logged_in_client, manufacturer, second_thread, project):
    # Arrange
    client, user = logged_in_client
    data = {
        'thread': second_thread.id,
        'quantity': 5.5,
    }
    url = reverse('threads:add_thread_project', kwargs={'manufacturer_slug': manufacturer.slug})

    # Act
    response = client.post(url, data=data, QUERY_STRING=f"project_id={project.id}", follow=False)

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:project_detail', args=[str(project.id)]) in response.url
    assert ProjectThread.objects.filter(
        project=project,
        thread=second_thread,
        quantity=5.5
    ).exists()


def test_add_thread_project_invalid_slug_returns_404(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:add_thread_project',
                                  kwargs={'manufacturer_slug': 'nonexistent-slug'}),
                          {'project_id': '123'})

    # Assert
    assert response.status_code == 404


def test_update_thread_project_authenticated_user(logged_in_client, first_project_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:update_thread_project',
                                  kwargs={'project_thread_id': first_project_thread.id}))

    # Assert
    assert response.status_code == 200
    assert response.context['title'].startswith('Запасы хомяка - ')
    assert response.context['project_thread'] == first_project_thread
    assert isinstance(response.context['form'], ThreadUpdateProjectForm)


def test_update_thread_project_unauthenticated_redirects(client, first_project_thread):
    # Act
    response = client.get(reverse('threads:update_thread_project',
                                  kwargs={'project_thread_id': first_project_thread.id}),
                          follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_update_thread_project_post_success(logged_in_client, first_project_thread, project):
    # Arrange
    client, user = logged_in_client
    data = {
        'quantity': 5.5,
    }

    # Act
    response = client.post(reverse('threads:update_thread_project',
                                   kwargs={'project_thread_id': first_project_thread.id}), data)

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:project_detail', args=[str(project.id)]) in response.url
    assert ProjectThread.objects.filter(
        project=project,
        thread=first_project_thread.thread,
        quantity=5.5
    ).exists()


def test_update_thread_project_invalid_project_thread_id_returns_404(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:update_thread_project',
                                  kwargs={'project_thread_id': 123}))

    # Assert
    assert response.status_code == 404


def test_delete_thread_project_post_success(logged_in_client, first_project_thread, project):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.post(reverse('threads:delete_thread_project',
                                   kwargs={'project_thread_id': first_project_thread.id}))

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:project_detail', args=[str(project.id)]) in response.url
    assert not ProjectThread.objects.filter(id=first_project_thread.id).exists()


def test_delete_thread_project_get_no_delete(logged_in_client, first_project_thread):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.get(reverse('threads:delete_thread_project',
                                  kwargs={'project_thread_id': first_project_thread.id}))

    # Assert
    assert response.status_code in (301, 302)
    assert reverse('threads:projects') in response.url
    assert ProjectThread.objects.filter(id=first_project_thread.id).exists()


def test_delete_thread_project_unauthenticated_redirects(client, first_project_thread):
    # Act
    response = client.get(reverse('threads:delete_thread_project',
                                  kwargs={'project_thread_id': first_project_thread.id}),
                          follow=False)

    # Assert
    assert response.status_code == 302
    assert '/user/login' in response.url


def test_delete_thread_project_invalid_project_thread_id_returns_404(logged_in_client):
    # Arrange
    client, user = logged_in_client

    # Act
    response = client.post(reverse('threads:delete_thread_project',
                                   kwargs={'project_thread_id': 123}))

    # Assert
    assert response.status_code == 404
