from django import forms
from threads.models import StockThread, BasketThread, Project, ProjectThread


class ThreadQuantityForm(forms.Form):
    """
    Форма для добавления количества ниток в хранилище.
    """
    quantity = forms.FloatField()
    thread = forms.IntegerField()


class ThreadUpdateStockForm(forms.ModelForm):
    """
    Форма для изменения количества ниток в запасе.
    """
    class Meta:
        model = StockThread
        fields = ('quantity',)


class ThreadUpdateBasketForm(forms.ModelForm):
    """
    Форма для изменения количества ниток в корзине.
    """
    class Meta:
        model = BasketThread
        fields = ('quantity',)


class ProjectForm(forms.ModelForm):
    """
    Форма для добавления проекта или изменения информации о проекте.
    """
    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'designer',
            'status',
            'owner',
        )


class ThreadUpdateProjectForm(forms.ModelForm):
    """
    Форма для изменения количества ниток в проекте.
    """
    class Meta:
        model = ProjectThread
        fields = ('quantity',)
