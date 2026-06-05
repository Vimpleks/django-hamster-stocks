from django.db import models
from django.contrib.auth.models import User
from .threads import Thread


class Basket(models.Model):
    """

    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        db_table = 'basket'
        verbose_name = 'Корзину'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'{self.id} - {self.owner.username}'


class BasketThread(models.Model):
    """

    """
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, verbose_name='Корзина')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, verbose_name='Нитка')
    quantity = models.FloatField('Количество', blank=False, null=False)

    class Meta:
        db_table = 'basket_thread'
        verbose_name = 'Корзину - Нитку'
        verbose_name_plural = 'Корзины - Нитки'
        constraints = [
            models.UniqueConstraint(
                fields=['basket', 'thread'],
                name='unique_basket_thread',
            )
        ]
