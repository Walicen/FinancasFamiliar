import datetime
import json
import stat

from builtins import round
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import logout_then_login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Fatura, Conta, Movimentacao, STATUS, Perfil, Sum
from .forms import FaturaForm, ContaForm, MovimentacaoForm, PerfilForm

def logout_view(request):
    logout_then_login(request,'')


class PerfilViewDetail(LoginRequiredMixin, DetailView):
    login_url = '/'
    model = Perfil
    form_class = PerfilForm
    template_name = 'perfil.html'


class Home(LoginRequiredMixin, View):
    login_url = '/'

    def get(self,  *args, **kwargs):

        data = Fatura.objects.dashboard()
        data['contas'] = Conta.objects.all(),
        data['atrasadas'] = Fatura.objects.filter(data_vencimento__lt=datetime.date.today(), status__isnull=True, tipo_fatura='D')

        return render(self.request, 'home.html', data)


class FaturaListView(LoginRequiredMixin, ListView):
    login_url = '/'
    model = Fatura
    context_object_name = 'faturas'
    paginate_by = 7


class FaturaPagarCreateView(LoginRequiredMixin,CreateView):
    login_url = '/'
    model = Fatura
    form_class = FaturaForm
    success_url = reverse_lazy('contas_fatura_list')


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
                            fatura.status = '3'
                            texto_mensagem = 'Lançamento quitado com sucesso'
                        fatura.save()
                        # atualizando conta
                        conta.save()
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
            'form': MovimentacaoForm(),
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
    paginate_by = 5


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
    form_class = ContaForm

