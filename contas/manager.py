import json
from datetime import datetime
from django.db import models
from django.db.models import Sum, Min, Max

class FaturaManager(models.Manager):

    def dashboard(self):
        data_atual = datetime.date.today()
        inicio = '01/{}/{} 00:00'.format(data_atual.month, data_atual.year)
        fim = '30/{}/{} 23:59'.format(data_atual.month, data_atual.year)
        inicio_mes = datetime.datetime.strptime(inicio, '%d/%m/%Y %H:%M')
        fim_mes = datetime.datetime.strptime(fim, '%d/%m/%Y %H:%M')
        labels = ['Receita prevista', 'Receita realizada']

        valores = [round(self.filter(data_vencimento__gte=inicio_mes, data_vencimento__lte=fim_mes,
                                               tipo_fatura='R').aggregate(Sum('valor_fatura'))['valor_fatura__sum'], 2),

                   round(self.filter(data_vencimento__gte=inicio_mes, data_vencimento__lte=fim_mes,
                                               tipo_fatura='R', status='2').aggregate(Sum('valor_fatura'))['valor_fatura__sum'], 2)

                   ]
        result = []

        for v in valores:
            if v is not None:
                result.append(v)
            else:
                result.append(0.00)

        data ={
            'labels': json.dumps(labels),
            'valores': json.dumps(valores),
        }

        return data