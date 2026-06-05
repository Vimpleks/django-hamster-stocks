from django.db import models
from django.contrib.auth.models import User
from .threads import Thread


class Project(models.Model):
    """

    """
    STATUS_CHOICES = [
        ('not started', 'не начат'),
        ('kitted', 'собран'),
        ('in progress', 'в работе'),
        ('complete', 'завершен'),
    ]

    name = models.CharField('Наименование', max_length=100, blank=False, null=False)
    description = models.CharField('Описание', max_length=500, blank=True, null=True)
    designer = models.CharField('Дизайнер', max_length=100, blank=True, null=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='not started'
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        db_table = 'project'
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return f'{self.name} - {self.owner.username}'


class ProjectThread(models.Model):
    """

    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, verbose_name='Нитка')
    quantity = models.FloatField('Количество', blank=False, null=False)

    class Meta:
        db_table = 'project_thread'
        verbose_name = 'Проект - Нитка'
        verbose_name_plural = 'Проекты - Нитки'
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'thread'],
                name='unique_project_thread',
            )
        ]
