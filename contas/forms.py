from django import forms
from django.forms import Textarea, TextInput

from .models import Fatura, Conta


class FaturaForm(forms.ModelForm):
    class Meta:
        model = Fatura
        fields = ['descricao', 'data_vencimento', 'valor_fatura']
        widgets = {
            'descricao': TextInput(attrs={'class': 'form-control form-control-alternative', 'placeholder': 'Descrição'}),
            'data_vencimento': TextInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Data Vencimento'}),
        }

class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['nome', 'tipo_conta', 'saldo_conta', 'usaurio']


