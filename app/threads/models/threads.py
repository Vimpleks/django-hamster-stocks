from django.db import models


class Manufacturers(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False, verbose_name='Наименование')
    is_public = models.BooleanField(default=True, verbose_name='Общий')

    class Meta:
        db_table = 'manufacturer'
        verbose_name = 'Производителя'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Threads(models.Model):
    article = models.CharField(max_length=50, blank=False, null=False, verbose_name='Артикул')
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Наименование')
    manufacturer = models.ForeignKey(Manufacturers, on_delete=models.CASCADE, verbose_name='Производитель')
    image = models.ImageField(upload_to='threads_images/', blank=True, null=True, verbose_name='Изображение')
    is_public = models.BooleanField(default=True, verbose_name='Общий')

    class Meta:
        db_table = 'thread'
        verbose_name = 'Нитку'
        verbose_name_plural = 'Нитки'

    def __str__(self):
        return f'{self.manufacturer} {self.name}'