from django.db import models
from django.contrib.auth.models import User
from .threads import Thread


class Stock(models.Model):
    """

    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        db_table = 'stock'
        verbose_name = 'Запас'
        verbose_name_plural = 'Запасы'

    def __str__(self):
        return f'{self.id} - {self.owner.username}'


class StockThread(models.Model):
    """

    """
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='Запас')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, verbose_name='Нитка')
    quantity = models.FloatField('Количество', blank=False, null=False)

    class Meta:
        db_table = 'stock_thread'
        verbose_name = 'Запас - Нитка'
        verbose_name_plural = 'Запасы - Нитки'
        constraints = [
            models.UniqueConstraint(
                fields=['stock', 'thread'],
                name='unique_stock_thread',
            )
        ]
