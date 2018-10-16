from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea, TextInput, DateInput, NumberInput, Select
from input_mask.fields import DecimalField

from .models import Fatura, Conta

'''
class FaturaForm(forms.Form):

    valor_fatura = forms.DecimalField(max_digits=10, localize=True, widget=TextInput(attrs={'class': 'money form-control form-control-alternative', 'placeholder': 'Valor Fatura'}))
    descricao = forms.CharField(widget=TextInput(attrs={'class': 'form-control form-control-alternative', 'placeholder': 'Descrição'}))
    data_vencimento = forms.DateField(widget=DateInput(attrs={'class': 'form-control', 'placeholder': 'Data Vencimento'}))
    
    descricao, data_vencimento, tipo_fatura, valor_fatura,
    
'''


class FaturaForm(forms.ModelForm):
    class Meta:
        model = Fatura
        fields = '__all__'
        exclude = {'conta', 'data_pagamento', 'valor_pago', 'desconto', 'juro', 'valor_total'}
        widgets = {
            'descricao': TextInput(attrs={
                                'class': 'form-control form-control-alternative',
                                'placeholder': 'Descrição',
                                }),
            'data_vencimento': DateInput(attrs={'id': 'ex',
                                'class': 'datepicker form-control form-control-alternative',
                                'placeholder': 'Data Vencimento'}),

            'tipo_fatura': Select(attrs={'class': 'form-control form-control-alternative',
                                         'placeholder': 'Tipo Conta',
                                        }),
            'valor_fatura': TextInput(attrs={
                'class': 'money form-control form-control-alternative',
                'placeholder': 'Valor'}),
        }
        localized_fields = {'valor_fatura'}

        labels = {
            'Descricao': 'Descrição',
            'data_vencimento': 'Data Vencimento',
            'tipo_fatura': 'Pagar / Receber',
            'valor_fatura': 'Valor'
        }
        '''
        def __init__(self, *args, **kwargs):
            super(FaturaForm, self).__init__(*args, **kwargs)
            self.fields['data_vencimento'].widget.format = '%d/%m/%Y'
        '''
class ContaForm(forms.ModelForm):
    class Meta:

        model = Conta

        fields = '__all__'

        labels = {'nome': 'Nome', 'tipo_conta': 'Tipo Conta', 'saldo_conta': 'Saldo', 'usuario': 'Usuário'}

        localized_fields = {'saldo_conta'}

        widgets = {
            'nome': TextInput(attrs={
                                'class': 'form-control form-control-alternative',
                                'placeholder': 'Nome',
                                }),
            'saldo_conta': TextInput(attrs={
                                'class': 'money form-control form-control-alternative',
                                'placeholder': 'Saldo',
                                'readonly': 'True'}),
            'usuario': Select(attrs={
                                'class': 'form-control form-control-alternative',
                                'placeholder': 'Usuário'}),
            'tipo_conta': Select(attrs={'class': 'form-control form-control-alternative',
                                        'placeholder': 'Tipo Conta',
                                        'label': 'Tipo Conta'}),
        }
