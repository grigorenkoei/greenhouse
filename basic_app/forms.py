from django.forms import ModelForm
from django import forms
from basic_app.models import Flat, FlatType


class FlatsForm(ModelForm):
    type = forms.ModelChoiceField(queryset=FlatType.objects.all(), label='Тип квартиры')

    class Meta:
        model = Flat
        fields = ['address', 'rent_price_month', 'price']
        labels = {'address': 'Адрес',
                  'rent_price_month': 'Стоимость квартиры',
                  'price': 'Цена в день'
                  }

        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Родимцева, 6', 'class':'col-xs-1'}),
            'rent_price_month': forms.NumberInput(attrs={'placeholder': '25000'}),
            'price': forms.NumberInput(attrs={'placeholder': '1700'}),
        }
