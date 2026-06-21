from django import forms
from threads.models import StockThread, BasketThread


class ThreadQuantityForm(forms.Form):
    quantity = forms.FloatField()
    thread = forms.IntegerField()


class ThreadUpdateStockForm(forms.ModelForm):
    class Meta:
        model = StockThread
        fields = ('quantity',)


class ThreadUpdateBasketForm(forms.ModelForm):
    class Meta:
        model = BasketThread
        fields = ('quantity',)
