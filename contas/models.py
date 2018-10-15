from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from django.db.models import *
from django.contrib.contenttypes.models import ContentType
from django.db import models as models


TIPO_FATURA = (
    ('P', 'Pagar'),
    ('R', 'Receber'),
)

TIPO_CONTA =(
    ('CC', 'Conta Corrente'),
    ('PO', 'Poupança'),
    ('CA', 'Carteira'),
)


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    cor = models.CharField(max_length=7)

class Conta(models.Model):

    # Fields
    nome = models.CharField(max_length=255)
    data_inclusao = models.DateTimeField(auto_now_add=True, editable=False)
    data_alteracao = models.DateTimeField(auto_now=True, editable=False)
    tipo_conta = models.CharField(max_length=2, choices=TIPO_CONTA)
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




def cria_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

#configurando o signal que detecta quando um usuario eh criado
#ao detectar, executa a funcao acima (cria_user_payer) para termos o
# "perfil" do jogador ligado ao usuario
# vide documentacao: https://docs.djangoproject.com/en/1.4/topics/auth/#storing-additional-information-about-users
post_save.connect(cria_perfil, sender=User)

