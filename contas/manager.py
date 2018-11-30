import simplejson as json

from django.db import models
from django.db.models import Sum, Min, Max
from django.db.models.functions import TruncMonth
from datetime import date

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



class FaturaManager(models.Manager):

    def gastos_realizados(self):
        gastos_ano = self.values('categoria').annotate(
            valor=Sum('valor_pago')).filter(tipo_fatura='D', data_vencimento__year=date.today().year).order_by()
        gastos={}
        for result in gastos_ano:
            i = int(result['categoria'])
            tupĺa = CATEGORIA[i - 1]
            gastos[tupĺa[1]] = result['valor']
        return gastos

    def previsao_faturas(self, ano, tipo):
        """ Retorna a previsão de faturas a pagar e receber tendo como parametros ano e tipo  """
        previstas = self.annotate(month=TruncMonth('data_vencimento')).values('month').annotate(
            valor=Sum('valor_fatura')).filter(tipo_fatura=tipo, data_vencimento__year=ano).order_by()
        # essa logica nao ficou muito pela minha falata de entendimento no orm do django assim que
        # eu tiver mais bagagem arrumo isso pq ta feio demais
        lista_valores = {
            1: 0.00,
            2: 0.00,
            3: 0.00,
            4: 0.00,
            5: 0.00,
            6: 0.00,
            7: 0.00,
            8: 0.00,
            9: 0.00,
            10: 0.00,
            11: 0.00,
            12: 0.00
        }
        for loop in range(1, 13):
            for p in previstas:
                d = p['month'].month
                if d == loop:
                    lista_valores[loop] = p['valor']

        lista = []

        for valor in lista_valores.values():
            lista.append(valor)
        return json.dumps(lista)
