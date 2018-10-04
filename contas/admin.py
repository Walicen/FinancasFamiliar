from django.contrib import admin
from django import forms
from .models import Fatura, Conta

class FaturaAdminForm(forms.ModelForm):

    class Meta:
        model = Fatura
        fields = '__all__'


class FaturaAdmin(admin.ModelAdmin):
    form = FaturaAdminForm
    list_display = ['descricao', 'data_inclusao', 'data_alteracao', 'data_vencimento', 'data_pagamento', 'tipo_fatura', 'valor_fatura', 'valor_pago', 'desconto', 'juro']
    readonly_fields = ['descricao', 'data_inclusao', 'data_alteracao', 'data_vencimento', 'data_pagamento', 'tipo_fatura', 'valor_fatura', 'valor_pago', 'desconto', 'juro']

admin.site.register(Fatura, FaturaAdmin)


class ContaAdminForm(forms.ModelForm):

    class Meta:
        model = Conta
        fields = '__all__'


class ContaAdmin(admin.ModelAdmin):
    form = ContaAdminForm
    list_display = ['nome', 'data_inclusao', 'data_alteracao', 'tipo_conta', 'saldo_conta']
    readonly_fields = ['nome', 'data_inclusao', 'data_alteracao', 'tipo_conta', 'saldo_conta']

admin.site.register(Conta, ContaAdmin)


