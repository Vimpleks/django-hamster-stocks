from django import forms
from threads.models import Thread, StockThread, BasketThread, Project, ProjectThread
from threads.fields import PositiveQuantityField


class ThreadQuantityForm(forms.Form):
    """
    Форма для добавления количества ниток в хранилище.
    """
    quantity = PositiveQuantityField()
    # thread = forms.IntegerField()
    thread = forms.ModelChoiceField(
        queryset=Thread.objects.all(),
        empty_label='Выберите нитку',
    )


class ThreadUpdateStockForm(forms.ModelForm):
    """
    Форма для изменения количества ниток в запасе.
    """
    quantity = PositiveQuantityField()

    class Meta:
        model = StockThread
        fields = ('quantity',)


class ThreadUpdateBasketForm(forms.ModelForm):
    """
    Форма для изменения количества ниток в корзине.
    """
    quantity = PositiveQuantityField()

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
        )


class ThreadUpdateProjectForm(forms.ModelForm):
    """
    Форма для изменения количества ниток в проекте.
    """
    quantity = PositiveQuantityField()

    class Meta:
        model = ProjectThread
        fields = ('quantity',)
