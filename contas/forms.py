from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea, TextInput, DateInput, NumberInput, Select
from input_mask.fields import DecimalField

from .models import Fatura, Conta, Movimentacao, CATEGORIA, TIPO_FATURA, Perfil


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = '__all__'
        exclude = {'data', 'fatura'}
        widgets = {

            'valor': TextInput(attrs={
                'class': 'money form-control form-control-alternative',
                'placeholder': 'Valor'}),

            'conta': Select(attrs={
                'class': 'form-control form-control-alternative',
                'placeholder': 'Conta'}),
        }

        localized_fields = {'valor'}


class FaturaForm(forms.ModelForm):

    class Meta:
        model = Fatura
        fields = '__all__'
        exclude = {'conta', 'data_pagamento', 'valor_pago', 'desconto', 'juro', 'valor_total', 'status'}
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
            'categoria': Select(attrs={'class': 'form-control form-control-alternative',
                                         'placeholder': 'Categoria',
                                         }),
        }
        localized_fields = {'valor_fatura'}

        labels = {
            'Descricao': 'Descrição',
            'data_vencimento': 'Data Vencimento',
            'tipo_fatura': 'Receitas / Despesas',
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


class ProjecaoForm(forms.Form):

    quantidade = forms.IntegerField(label='Quantidade Parcelas', initial=1,
                                    widget=forms.TextInput(attrs={'placeholder': 'quantidade',
                                                                   'class': 'form-control form-control-alternative'}))

    descricao = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Descrição',
                                                             'class': 'form-control form-control-alternative'}))
    data_inicial = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker form-control form-control-alternative',
                                                                 'placeholder': 'Data Vencimento'}))

    tipo = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control form-control-alternative',
                                                        'placeholder': 'Tipo Fatura'}), label='Tipo Fatura', choices=[('R', 'RECEITA'),('D', 'DESPESA')])

    valor = forms.DecimalField(widget=forms.TextInput(attrs={
                'class': 'money form-control form-control-alternative',
                'placeholder': 'Valor'}), localize=True, label='Valor Documento')

    categoria = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control form-control-alternative',
                                                             'placeholder': 'Categoria'}), choices=[('1', 'Educação'),
    ('2', 'Alimentação'),
    ('3', 'Automóvel'),
    ('4', 'Lazer'),
    ('5', 'Sálario'),
    ('6', 'Impostos'),
    ('7', 'Farmácia'),
    ('8', 'Moradia'),
    ('9', 'Vestuário'),
    ('10', 'Outros')])


class PesquisaFaturaForm(forms.Form):

    descricao = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Descrição',
                                                              'class': 'form-control form-control-alternative'}), required=False)

    data_inicial = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker form-control form-control-alternative',
                                      'placeholder': 'Periodo Inicio'}), label="Data Inicial")

    data_final = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker form-control form-control-alternative',
                                       'placeholder': 'Periodo Fim'}), label='Data Fim')



class TransferenciaForm(forms.Form):

    conta_sair = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control form-control-alternative',
                                                        'placeholder': 'Conta Saída'}), label='Conta Saída',
                                          queryset=Conta.objects.all())

    conta_entrada = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control form-control-alternative',
                                                                     'placeholder': 'Conta Entrada'}),
                                          label='Conta Entrada', queryset=Conta.objects.all())

    valor = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': 'money form-control form-control-alternative',
        'placeholder': 'Valor'}), localize=True, label='Valor Transferência')