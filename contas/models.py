from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import *
from django.contrib.contenttypes.models import ContentType
from django.db import models as models


TIPO_FATURA = (
    ('P', 'Pagar'),
    ('R', 'Receber'),
)

class Conta(models.Model):

    # Fields
    nome = models.CharField(max_length=255)
    data_inclusao = models.DateTimeField(auto_now_add=True, editable=False)
    data_alteracao = models.DateTimeField(auto_now=True, editable=False)
    tipo_conta = models.CharField(max_length=30)
    saldo_conta = models.DecimalField( max_digits = 10 , decimal_places = 2)

    # Relationship Fields
    usaurio = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'conta'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('contas_conta_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('contas_conta_update', args=(self.pk,))


class Fatura(models.Model):
    # Fields
    descricao = models.CharField(max_length=255)
    data_inclusao = models.DateTimeField(auto_now_add=True, editable=False)
    data_alteracao = models.DateTimeField(auto_now=True, editable=False)
    data_vencimento = models.DateTimeField(null=False)
    data_pagamento = models.DateTimeField(null=True)
    tipo_fatura = models.CharField(max_length=1, choices=TIPO_FATURA)
    valor_fatura = models.DecimalField( max_digits = 10 , decimal_places = 2)
    valor_pago = models.DecimalField( max_digits = 10 , decimal_places = 2, null=True)
    desconto = models.DecimalField( max_digits = 10 , decimal_places = 2, null=True)
    juro = models.DecimalField( max_digits = 10 , decimal_places = 2, null=True)
    valor_total = models.DecimalField( max_digits = 10 , decimal_places = 2, null=True)

    conta = ForeignKey(Conta, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'fatura'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('contas_fatura_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('contas_fatura_update', args=(self.pk,))





