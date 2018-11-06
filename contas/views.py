import datetime

from django.contrib.auth import logout
from django.contrib.auth.views import logout_then_login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Fatura, Conta, Movimentacao, STATUS
from .forms import FaturaForm, ContaForm, MovimentacaoForm


def logout_view(request):
    logout_then_login(request,'')

class Home(View):
    def get(self,  *args, **kwargs):
        return render(self.request, 'home.html',{'contas': Conta.objects.all()})

class FaturaQuitar():

    def get(self, *args, **kwargs):
        pass


class FaturaListView(ListView):
    model = Fatura
    context_object_name = 'faturas'
    paginate_by = 7


class FaturaPagarCreateView(CreateView):
    model = Fatura
    form_class = FaturaForm
    success_url = reverse_lazy('contas_fatura_list')


class MovimentacaoView(View):

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
                    if fatura.tipo_fatura == 'R':
                        conta.saldo_conta += valor
                    else:
                        conta.saldo_conta -= valor

                    conta.save()
                else:
                    texto_mensagem = 'Valor do lançamento maior que o valor da fatura!'
            else:
                texto_mensagem = 'Valor da movimentação deve ser maior que zero!'


        data = {
            'texto_mensagem': texto_mensagem,
            'texto_erro': texto_erro,
            'fatura': fatura,
            'form': MovimentacaoForm(),
            'lista': fatura.movimentacoes.all()
        }

        return render(request, 'contas/fatura_detail.html', data)


class FaturaDetailView(View):

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



class FaturaUpdateView(UpdateView):
    model = Fatura
    form_class = FaturaForm


class ContaListView(ListView):
    context_object_name = 'contas'
    model = Conta
    paginate_by = 5


class ContaCreateView(CreateView):
    model = Conta
    form_class = ContaForm
    success_url = reverse_lazy('contas_conta_list')

class ContaDetailView(DetailView):
    model = Conta


class ContaUpdateView(UpdateView):
    model = Conta
    form_class = ContaForm

