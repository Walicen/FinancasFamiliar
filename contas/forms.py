from django import forms
from .models import Fatura, Conta


class FaturaForm(forms.ModelForm):
    class Meta:
        model = Fatura
        fields = ['Descricao', 'data_vencimento', 'data_pagamento', 'tipo_fatura', 'valor_fatura', 'valor_pago', 'desconto', 'juro']


class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['nome', 'tipo_conta', 'saldo_conta', 'usaurio']


