from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Fatura, Conta
from .forms import FaturaForm, ContaForm


class FaturaListView(ListView):
    model = Fatura


class FaturaCreateView(CreateView):
    model = Fatura
    form_class = FaturaForm


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

