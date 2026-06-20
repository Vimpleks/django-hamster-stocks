from django.db import models


class Manufacturer(models.Model):
    """
    Производитель нитки.
    Отдельная модель, чтобы не хранить производителя как строку в каждой нитке.
    """
    name = models.CharField(
        'Наименование',
        max_length=50,
        unique=True,
        blank=False,
        null=False
    )
    is_public = models.BooleanField('Общий', default=True)
    slug = models.SlugField('Slug', unique=True)

    class Meta:
        db_table = 'manufacturer'
        verbose_name = 'Производителя'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Thread(models.Model):
    """
    Нитка — центральная модель проекта.

    Связана с Manufacturer через ForeignKey (много ниток → один производитель).
    """
    article = models.CharField('Артикул', max_length=50, blank=False, null=False)
    name = models.CharField('Наименование', max_length=100, blank=True, null=True)
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        verbose_name='Производитель'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='threads_images/',
        blank=True,
        null=True
    )
    is_public = models.BooleanField(verbose_name='Общий', default=True)
    slug = models.SlugField('Slug', unique=True)

    class Meta:
        db_table = 'thread'
        verbose_name = 'Нитку'
        verbose_name_plural = 'Нитки'
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'manufacturer'],
                name='unique_thread_article_manufacturer',
            )
        ]

    def __str__(self):
        return f'{self.manufacturer} {self.article}'
