from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Fatura, Conta, Perfil


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


admin.site.register(Conta, ContaAdmin)

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
