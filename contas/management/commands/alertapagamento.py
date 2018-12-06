from django.core.mail import send_mail
from django.core.management import BaseCommand

from contas.models import Fatura
from datetime import date

class Command(BaseCommand):
    help = 'Verificar contas a vencer'

    def add_arguments(self, parser):
        parser.add_argument('operacao', nargs='+', type=int)

    def handle(self, *args, **options):
        for op in options['operacao']:
            if op == 1:

                atrasadas = list(Fatura.objects.filter(data_vencimento__lt=date.today(), status__isnull=True, tipo_fatura='D'))
                vencimentos_hoje = list(Fatura.objects.filter(data_vencimento=date.today(), status__isnull=True, tipo_fatura='D'))
                lista = []
                lista.append('Atrasadas: ')
                if atrasadas:
                    for fatura in atrasadas:
                        lista.append('\n {} - valor: {} R$'.format(fatura.descricao, fatura.valor_fatura))
                else:
                    lista.append('\n Sem Lançamentos atrasados\n')

                lista.append('Vencimentos Hoje: ')

                if vencimentos_hoje:
                    for fatura in vencimentos_hoje:
                        lista.append('\n {} - valor: R$'.format(fatura.descricao, fatura.valor_fatura))
                else:
                    lista.append('\n Sem vencimentos hoje\n')

                send_mail(
                    'Financeiro Familiar',  # Assunto
                    ''.join(lista),  # Corpo
                    'diegodenzer.devops@gmail.com',
                    ['diegodenzer.devops@gmail.com', 'simonetn.eng@hotmail.com']
                )
                self.stdout.write(self.style.SUCCESS('Enviando'))


