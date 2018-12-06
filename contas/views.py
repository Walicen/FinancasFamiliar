import calendar
from datetime import *
from datetime import date
from django.core.mail import BadHeaderError, send_mail
import simplejson as json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, CreateView

from .forms import FaturaForm, ContaForm, MovimentacaoForm, PerfilForm, ProjecaoForm, PesquisaFaturaForm, \
    TransferenciaForm
from .models import Fatura, Conta, Movimentacao, Perfil


def logout_view(request):
    logout_then_login(request, '')


class PerfilViewDetail(LoginRequiredMixin, View):
    login_url = '/'
    template_name = 'contas/perfil.html'


class Home(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):

        label = ['Jan', 'Fev', 'Mar', 'Abril', 'Mai', 'Jun', 'Jul', 'Set', 'Ago', 'Out', 'Nov', 'Dez']
        receitas = Fatura.objects.previsao_faturas(date.today().year, 'R')
        despesas = Fatura.objects.previsao_faturas(date.today().year, 'D')

        gastos = Fatura.objects.gastos_realizados()

        labelGrafico2 = []
        valoresGrafico2 = []
        for key in gastos.keys():
            labelGrafico2.append(key)

        for key in gastos.values():
            valoresGrafico2.append(key)



        data = {
            'receitas': receitas,
            'despesas': despesas,
            'contas': Conta.objects.all(),
            'labels': json.dumps(label),
            'atrasadas': Fatura.objects.filter(data_vencimento__lt=date.today(), status__isnull=True, tipo_fatura='D'),
            'labels2': json.dumps(labelGrafico2),
            'valores2': json.dumps(valoresGrafico2)
        }

        return render(request, 'home.html', data)


class FaturaListView(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request):
        form = PesquisaFaturaForm(request.POST)
        if form.is_valid():
            inicio = form.cleaned_data['data_inicial']
            fim = form.cleaned_data['data_final']
            descricao = form.cleaned_data['descricao']

        if descricao is not None:
            fatura_list = Fatura.objects.filter(data_vencimento__gte=inicio,
                                                data_vencimento__lte=fim,
                                                descricao__icontains=descricao).order_by(
                'data_vencimento')
        else:
            fatura_list = Fatura.objects.filter(data_vencimento__gte=inicio, data_vencimento__lte=fim).order_by(
                'data_vencimento')

        paginator = Paginator(fatura_list, 10)

        page = request.GET.get('page')
        faturas = paginator.get_page(page)

        context = {
            'faturas': faturas,
            'form': form
        }

        return render(request, 'contas/fatura_list.html', context)

    def get(self, request):

        hoje = date.today()

        inicio = date.fromordinal(hoje.toordinal() - 45)  # hoje - 45 dias

        fim = date.fromordinal(hoje.toordinal() + 45)  # hoje + 45 dias

        form = PesquisaFaturaForm(initial={'data_inicial': inicio , 'data_final': fim})

        fatura_list = Fatura.objects.filter(data_vencimento__gte=inicio, data_vencimento__lte=fim).order_by('data_vencimento')

        paginator = Paginator(fatura_list, 10)

        page = request.GET.get('page')

        faturas = paginator.get_page(page)

        context = {
            'faturas': faturas,
            'form': form
        }

        return render(request, 'contas/fatura_list.html', context)


class FaturaPagarCreateView(LoginRequiredMixin,CreateView):
    login_url = '/'
    model = Fatura
    form_class = FaturaForm
    #success_url = reverse_lazy('contas_fatura_list')


class MovimentacaoView(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request, fatura):
        texto_erro = ''
        texto_mensagem = ''
        fatura = Fatura.objects.get(pk=fatura)
        form = MovimentacaoForm(request.POST)

        if form.is_valid():

            conta = form.cleaned_data['conta']
            valor = form.cleaned_data['valor']

            if valor > 0:

                if fatura.valor_fatura >= fatura.valor_pago + valor:
                    movimenta = True
                    if conta.tipo_conta == 'CA':
                        if conta.saldo_conta >= valor:
                            if fatura.tipo_fatura == 'R':
                                conta.saldo_conta += valor
                            else:
                                conta.saldo_conta -= valor
                        else:
                            movimenta = False
                            texto_erro = 'Carteira sem saldo suficiente!'
                    else:
                        if fatura.tipo_fatura == 'R':
                            conta.saldo_conta += valor
                        else:
                            conta.saldo_conta -= valor


                    if movimenta:
                        movimentacao = Movimentacao.objects.create(
                            fatura=fatura,
                            valor=valor,
                            conta=conta
                        )
                        # atualizando fatura
                        fatura.valor_pago += valor
                        if fatura.valor_pago == fatura.valor_fatura:
                            fatura.status = '2'
                            texto_mensagem = 'Lançamento quitado com sucesso'

                        fatura.save()
                        # atualizando conta
                        conta.save()

                        send_mail(
                            'TEste 1',# Assunto
                            'Lançamento {} quitado com sucesso'.format(fatura.descricao), # Corpo
                            'diegodenzer.devops@gmail.com',
                            ['diegodenzer.devops@gmail.com']
                        )
                else:
                    texto_erro = 'Valor do lançamento maior que o valor da fatura!'
            else:
                texto_erro = 'Valor da movimentação deve ser maior que zero!'


        data = {
            'texto_mensagem': texto_mensagem,
            'texto_erro': texto_erro,
            'fatura': fatura,
            'form': MovimentacaoForm(),
            'lista': fatura.movimentacoes.all()
        }

        return render(request, 'contas/fatura_detail.html', data)


class FaturaDetailView(LoginRequiredMixin,View):
    login_url = '/'
    def get(self, request, pk):
        fatura = Fatura.objects.get(pk=pk)
        movimentacoes = Movimentacao.objects.filter(fatura=fatura.pk)
        data = {
            'fatura': fatura,
            'form': MovimentacaoForm(initial={'valor': fatura.valor_fatura}),
            'lista': movimentacoes
        }
        return render(request, 'contas/fatura_detail.html', data)

    def post(self, request, pk):
        pass


class FaturaUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/'
    model = Fatura
    form_class = FaturaForm


class ContaListView(LoginRequiredMixin, ListView):
    login_url = '/'
    context_object_name = 'contas'
    model = Conta
    paginate_by = 10


class ContaCreateView(LoginRequiredMixin, CreateView):
    login_url = '/'
    model = Conta
    form_class = ContaForm
    success_url = reverse_lazy('contas_conta_list')


class ContaDetailView(LoginRequiredMixin, DetailView):
    login_url = '/'
    model = Conta


class ContaUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/'
    model = Conta
    context_object_name = 'conta'
    form_class = ContaForm


class ProjecaoView(LoginRequiredMixin, View):

    login_url = '/'
    def get(self, request):
        form = ProjecaoForm()
        data = {
            'form': form,
        }
        return render(request, 'contas/projecao.html', data)

    def post(self, request):
        form = ProjecaoForm(request.POST)
        if form.is_valid():

            hoje = form.cleaned_data['data_inicial']
            dia = hoje.day
            mes = hoje.month
            ano = hoje.year

            for f in range(1, form.cleaned_data['quantidade']+1):
                fatura = Fatura()
                if f == 0:
                    fatura.data_vencimento = form.cleaned_data['data_inicial']
                    mes += 1
                else:
                    fim_mes = calendar.monthrange(ano, mes)
                    if dia > 28 and mes == 2:
                        temp_dia = 28
                        dia_vencimento = '{}/{}/{} 12:00'.format(temp_dia, mes, ano)
                    elif dia == 31 and fim_mes[1] == 30:
                        temp_dia = 30
                        dia_vencimento = '{}/{}/{} 12:00'.format(temp_dia, mes, ano)
                    else:
                        dia_vencimento = '{}/{}/{} 12:00'.format(dia, mes, ano)

                    data = datetime.strptime(dia_vencimento, '%d/%m/%Y %H:%M')
                    fatura.data_vencimento = data

                    if mes == 12:
                        mes = 1
                        ano += 1
                    else:
                        mes += 1

                fatura.categoria = form.cleaned_data['categoria']
                fatura.valor_fatura = form.cleaned_data['valor']
                fatura.tipo_fatura = form.cleaned_data['tipo']
                fatura.status = '1'
                fatura.descricao = "{} - {} de {}".format(form.cleaned_data['descricao'], f, form.cleaned_data['quantidade'])
                fatura.save()

            return redirect('contas_fatura_list')
        else:
            data = {
                'form': form,
            }
            return render(request, 'contas/projecao.html', data)

class TransferenciaView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self,request):
        return render(request,'contas/transferencia.html', {'form': TransferenciaForm()})

    def post(self,request):

        form = TransferenciaForm(request.POST)

        if form.is_valid():
            conta_entrada = form.cleaned_data['conta_entrada']
            conta_saida = form.cleaned_data['conta_sair']
            valor = form.cleaned_data['valor']
            if conta_entrada.id == conta_saida.id:
                return render(request, 'contas/transferencia.html', {'form': form, 'msg_erro': 'Conta igual para entrada e saída'})
            else:
                if conta_saida.saldo_conta < valor:
                    return render(request, 'contas/transferencia.html', {'form': form, 'msg_erro': 'Conta saída sem saldo para transferência.'})
                else:
                    conta_entrada.saldo_conta += valor
                    conta_saida.saldo_conta -= valor
                    conta_entrada.save()
                    conta_saida.save()

                    return render(request, 'contas/transferencia.html', {'form': TransferenciaForm(), 'msg_sucesso': 'Transferência realizada com sucesso'})
        else:
            return render(request, 'contas/transferencia.html', {'form': form})


class UserUpdateView(LoginRequiredMixin, DetailView):
    login_url = '/'
    model = User
    template_name = 'contas/perfil.html'
