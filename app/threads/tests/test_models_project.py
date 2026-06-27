import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DataError

from threads.models import Project, ProjectThread


def test_create_project_user_relationship(user):
    # Act
    project = Project.objects.create(
        name='Акварельные домики',
        description='Похожи на норвежские домики',
        designer='Наталья Юркевич',
        status='kitted',
        owner=user,
    )

    # Assert
    assert project.name == 'Акварельные домики'
    assert project.designer == 'Наталья Юркевич'
    assert project.status == 'kitted'
    assert project.owner == user
    assert project.id is not None


def test_project_name_max_length(user):
    # Assert
    with pytest.raises(DataError):
        Project.objects.create(name='А' * 101, owner=user)


def test_project_full_clean_not_valid_status(project):
    # Act
    project.status = 'invalid'

    # Assert
    with pytest.raises(ValidationError):
        project.full_clean()


def test_project_user_cascade_delete(user, project):
    # Act
    user.delete()

    # Assert
    assert not Project.objects.filter(id=project.id).exists()


def test_project_str(project):
    # Assert
    assert str(project) == 'Акварельные домики - testuser'


def test_create_project_thread(project, first_thread):
    # Act
    project_thread = ProjectThread.objects.create(
        project=project,
        thread=first_thread,
        quantity=1.5
    )

    # Assert
    assert project_thread.quantity == 1.5
    assert project_thread.id is not None


def test_project_thread_project_relationship(first_project_thread, project):
    # Assert
    assert first_project_thread.project == project


def test_project_thread_thread_relationship(first_project_thread, first_thread):
    # Assert
    assert first_project_thread.thread == first_thread


def test_project_thread_sproject_cascade_delete(first_project_thread, project):
    # Act
    project.delete()

    # Assert
    assert not ProjectThread.objects.filter(id=first_project_thread.id).exists()


def test_project_thread_thread_cascade_delete(first_project_thread, first_thread):
    # Act
    first_thread.delete()

    # Assert
    assert not ProjectThread.objects.filter(id=first_project_thread.id).exists()


def test_project_thread_unique(first_project_thread, project, first_thread):
    # Assert
    with pytest.raises(IntegrityError):
        ProjectThread.objects.create(project=project, thread=first_thread, quantity=2)
