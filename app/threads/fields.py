from django import forms


class PositiveQuantityField(forms.FloatField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('min_value', 0.01)
        super().__init__(*args, **kwargs)
