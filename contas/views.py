import datetime
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Fatura, Conta
from .forms import FaturaForm, ContaForm


class FaturaListView(ListView):
    model = Fatura
    context_object_name = 'faturas'

class FaturaCreateView(View):
    model = Fatura

    def get(self, *args, **kwargs):
        form = FaturaForm()
        form.data_vencimento = datetime.datetime.now()
        form.descricao ='teste'
        data = {
            'form': form,
        }

        return render(self.request, 'contas/fatura_form.html', data)

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

