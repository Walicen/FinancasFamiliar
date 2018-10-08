import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Fatura, Conta
from .forms import FaturaForm, ContaForm


class FaturaListView(ListView):
    model = Fatura
    context_object_name = 'faturas'

class FaturaPagarCreateView(View):
    model = Fatura

    def get(self, *args, **kwargs):
        form = FaturaForm()
        data = {
            'form': form,
        }

        return render(self.request, 'contas/fatura_form.html', data)

    def post(self, *args, **kwargs):
        form = self.request.POST or None
        fatura = Fatura()
        fatura.tipo_fatura = 'P'
        fatura.descricao = form['descricao']
        fatura.data_vencimento = form['data_vencimento']
        fatura.valor_fatura = form['valor_fatura']
        fatura.save()
        return redirect('contas_fatura_list')


class FaturaDetailView(DetailView):
    model = Fatura


class FaturaUpdateView(UpdateView):
    model = Fatura
    form_class = FaturaForm


class ContaListView(ListView):
    model = Conta


class ContaCreateView(CreateView):
    model = Conta
    form_class = ContaForm


class ContaDetailView(DetailView):
    model = Conta


class ContaUpdateView(UpdateView):
    model = Conta
    form_class = ContaForm

