from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea, TextInput, DateInput, NumberInput, Select
from input_mask.fields import DecimalField

from .models import Fatura, Conta


class FaturaForm(forms.Form):

    valor_fatura = forms.DecimalField(max_digits=10, localize=True, widget=TextInput(attrs={'class': 'money form-control form-control-alternative', 'placeholder': 'Valor Fatura'}))
    descricao = forms.CharField(widget=TextInput(attrs={'class': 'form-control form-control-alternative', 'placeholder': 'Descrição'}))
    data_vencimento = forms.DateField(widget=DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Data Vencimento'}))

class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['nome', 'tipo_conta', 'saldo_conta', 'usaurio']

        widgets = {
            'nome': TextInput(attrs={'class': 'form-control form-control-alternative', 'placeholder': 'Nome'}),
            'saldo_conta': TextInput(attrs={'class': 'money form-control form-control-alternative', 'placeholder': 'Valor Fatura'}),
            'usaurio': Select(attrs={'class': 'form-control form-control-alternative'}),
            'tipo_conta': Select(attrs={'class': 'form-control form-control-alternative'}),
        }
