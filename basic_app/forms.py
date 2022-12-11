from django.forms import ModelForm
from django import forms
from basic_app.models import Flat, FlatType, Order


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


class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=255,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'aria-label': 'First name'}))
    last_name = forms.CharField(max_length=255,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'aria-label': 'First name'}))

    address = forms.ModelChoiceField(Flat.objects.all(),
                                     empty_label="Выберите адрес",
                                     widget=forms.Select(attrs={'class': 'form-control'}))

    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                                              'class': 'form-control'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                                            'class': 'form-control'}))

    discount_card = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                       'placeholder': '12345678'}))

    phone_number = forms.CharField(max_length=12,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': '89228352422'
                                                                 }))
    price = forms.IntegerField(label='exampleFormControlInput1',
                               widget=forms.NumberInput(attrs={'class': 'form-control',
                                                               'placeholder': '2200'
                                                               }))
    desc = forms.CharField(max_length=100, label='exampleFormControlInput1',
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'placeholder': 'Информация о клиенте...',
                                                        'rows': 3,
                                                        'cols': 3
                                                        }))


