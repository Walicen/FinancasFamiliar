from django.contrib.auth.models import User
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.db.models import *
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields

TIPO_FATURA = (
    ('P', 'Pagar'),
    ('R', 'Receber'),
)

class Fatura(models.Model):

    # Fields
    descricao = models.CharField(max_length=255)
    data_inclusao = models.DateTimeField(auto_now_add=True, editable=False)
    data_alteracao = models.DateTimeField(auto_now=True, editable=False)
    data_vencimento = models.DateTimeField(null=False)
    data_pagamento = models.DateTimeField()
    tipo_fatura = models.CharField(max_length=1, choices=TIPO_FATURA)
    valor_fatura = models.FloatField(default=0)
    valor_pago = models.FloatField(default=0)
    desconto = models.FloatField(default=0)
    juro = models.FloatField(default=0)
    valor_total = models.FloatField(default=0)


    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('contas_fatura_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('contas_fatura_update', args=(self.pk,))


class Conta(models.Model):

    # Fields
    nome = models.CharField(max_length=255)
    data_inclusao = models.DateTimeField(auto_now_add=True, editable=False)
    data_alteracao = models.DateTimeField(auto_now=True, editable=False)
    tipo_conta = models.CharField(max_length=30)
    saldo_conta = models.FloatField()

    # Relationship Fields
    usaurio = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('contas_conta_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('contas_conta_update', args=(self.pk,))


