import simplejson as json
from  datetime import *
from django.db import models
from django.db.models import Sum, Min, Max
from django.db.models.functions import TruncMonth


class FaturaManager(models.Manager):

    def novo_dash(self):

        data_atual = date.today()

        teste = self.annotate(month=TruncMonth('data_vencimento')).values('month').annotate(c=Sum('valor_fatura')).order_by()
        list = {}
        for t in teste:
            data = t['month']
            valor = t['c']
            list[data.month] = valor


        return json.dumps(list)



    def dashboard(self):
        data_atual = date.today()
        inicio = '01/{}/{} 00:00'.format(data_atual.month, data_atual.year)
        fim = '30/{}/{} 23:59'.format(data_atual.month, data_atual.year)
        inicio_mes = datetime.strptime(inicio, '%d/%m/%Y %H:%M')
        fim_mes = datetime.strptime(fim, '%d/%m/%Y %H:%M')

        valores = [self.filter(data_vencimento__gte=inicio_mes, data_vencimento__lte=fim_mes, tipo_fatura='R')
                       .aggregate(Sum('valor_fatura'))['valor_fatura__sum'],

                   self.filter(data_vencimento__gte=inicio_mes, data_vencimento__lte=fim_mes, tipo_fatura='R', status='2')
                       .aggregate(Sum('valor_fatura'))['valor_fatura__sum'],

                   self.filter(data_vencimento__gte=inicio_mes, data_vencimento__lte=fim_mes, tipo_fatura='D')
                       .aggregate(Sum('valor_fatura'))['valor_fatura__sum'],
                   self.filter(data_vencimento__gte=inicio_mes, data_vencimento__lte=fim_mes, tipo_fatura='D', status='2')
                       .aggregate(Sum('valor_fatura'))['valor_fatura__sum'],

                   ]

        result = []

        for v in valores:
            if v is not None:
                result.append(v)
            else:
                result.append(0.00)

        return json.dumps(valores)