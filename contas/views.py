import datetime

from django.contrib.auth import logout
from django.contrib.auth.views import logout_then_login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Fatura, Conta
from .forms import FaturaForm, ContaForm


def logout_view(request):
    logout_then_login(request,'')

class Home(View):
    def get(self,  *args, **kwargs):
        return render(self.request, 'home.html',{})

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


class FaturaDetailView(DetailView):
    model = Fatura


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

