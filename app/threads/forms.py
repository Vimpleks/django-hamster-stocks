from django import forms
from threads.models import StockThread, BasketThread, Project, ProjectThread


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


class ProjectForm(forms.ModelForm):
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
    class Meta:
        model = ProjectThread
        fields = ('quantity',)
