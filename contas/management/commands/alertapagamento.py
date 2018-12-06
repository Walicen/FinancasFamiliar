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
                faturas = list(Fatura.objects.filter(data_vencimento__lt=date.today(), status__isnull=True, tipo_fatura='D'))
                for fatura in faturas:

                    send_mail(
                        'Teste 1',  # Assunto
                        'Atrasada {}'.format(fatura.descricao),  # Corpo
                        'diegodenzer.devops@gmail.com',
                        ['diegodenzer.devops@gmail.com']
                    )
                    self.stdout.write(self.style.SUCCESS('Enviando'))


