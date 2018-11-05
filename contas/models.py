from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from django.db.models import *
from django.contrib.contenttypes.models import ContentType
from django.db import models as models

CATEGORIA = (
    ('1', 'Educação',),
    ('2', 'Alimentação',),
    ('3', 'Automóvel'),
    ('4', 'Lazer'),
    ('5', 'Sálario'),
    ('6', 'Impostos'),
    ('7', 'Farmácia'),
    ('8', 'Moradia'),
    ('9', 'Vestuário'),
    ('10', 'Outros')
)


TIPO_FATURA = (
    ('R', 'RECEITA'),
    ('D', 'DESPESA'),
)

TIPO_CONTA = (
    ('CC', 'Conta Corrente'),
    ('PO', 'Poupança'),
    ('CA', 'Carteira'),
)

STATUS = (
    ('PE', 'Pendente'),
    ('PG', 'Paga'),
    ('VE', 'Vencida'),
)


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    cor = models.CharField(max_length=7)


class Conta(models.Model):
    ''' Modelo para Contas '''
    nome = models.CharField(max_length=255)
    data_inclusao = models.DateTimeField(auto_now_add=True, editable=False)
    data_alteracao = models.DateTimeField(auto_now=True, editable=False)
    tipo_conta = models.CharField(max_length=2, choices=TIPO_CONTA)
    saldo_conta = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # relacionamento
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

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
    ''' Modelo para as faturas '''
    descricao = models.CharField(max_length=255)
    data_inclusao = models.DateTimeField(auto_now_add=True, editable=False)
    data_alteracao = models.DateTimeField(auto_now=True, editable=False)
    data_vencimento = models.DateTimeField(null=False)
    data_pagamento = models.DateTimeField(null=True)
    tipo_fatura = models.CharField(max_length=2, choices=TIPO_FATURA)
    valor_fatura = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    juro = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    status = models.CharField(max_length=1, choices=STATUS, null=True)
    categoria = models.CharField(max_length=1, choices=CATEGORIA, null=True, blank=True)

    # relacionamento
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


class Movimentacao(models.Model):
    data = models.DateTimeField(auto_now_add=True, editable=False)
    conta = ForeignKey(Conta, on_delete=models.CASCADE)
    fatura = ForeignKey(Fatura, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'movimentacao'
        ordering = ('-pk',)

def cria_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

# configurando o signal que detecta quando um usuario eh criado
# ao detectar, executa a funcao acima (cria_user_payer) para termos o
# "perfil" do jogador ligado ao usuario
post_save.connect(cria_perfil, sender=User)
