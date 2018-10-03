from . import models

from rest_framework import serializers


class FaturaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Fatura
        fields = (
            'pk', 
            'Descricao', 
            'data_inclusao', 
            'data_alteracao', 
            'data_vencimento', 
            'data_pagamento', 
            'tipo_fatura', 
            'valor_fatura', 
            'valor_pago', 
            'desconto', 
            'juro', 
        )


class ContaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Conta
        fields = (
            'pk', 
            'nome', 
            'data_inclusao', 
            'data_alteracao', 
            'tipo_conta', 
            'saldo_conta', 
        )


