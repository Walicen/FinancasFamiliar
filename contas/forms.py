from django import forms
from django.forms import Textarea, TextInput, DateInput, NumberInput
from input_mask.fields import DecimalField

from .models import Fatura, Conta


class FaturaForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(FaturaForm, self).__init__(*args, **kwargs)
        self.fields['valor_fatura'].localize = True
        self.fields['valor_fatura'].widget.is_localized = True

    valor_fatura = forms.DecimalField(max_digits=10, decimal_places=2, localize=True, widget=TextInput(attrs={'class': 'money form-control','placeholder': 'Valor Fatura'}))
    descricao = forms.CharField(widget=TextInput(attrs={'class': 'form-control form-control-alternative', 'placeholder': 'Descrição'}))
    data_vencimento = forms.DateField(widget=DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Data Vencimento'}))

class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['nome', 'tipo_conta', 'saldo_conta', 'usaurio']


