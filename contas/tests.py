import unittest
from django.urls import reverse
from django.test import Client
from .models import Fatura, Conta
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_fatura(**kwargs):
    defaults = {}
    defaults["Descricao"] = "Descricao"
    defaults["data_vencimento"] = "data_vencimento"
    defaults["data_pagamento"] = "data_pagamento"
    defaults["tipo_fatura"] = "tipo_fatura"
    defaults["valor_fatura"] = "valor_fatura"
    defaults["valor_pago"] = "valor_pago"
    defaults["desconto"] = "desconto"
    defaults["juro"] = "juro"
    defaults.update(**kwargs)
    return Fatura.objects.create(**defaults)


def create_conta(**kwargs):
    defaults = {}
    defaults["nome"] = "nome"
    defaults["tipo_conta"] = "tipo_conta"
    defaults["saldo_conta"] = "saldo_conta"
    defaults.update(**kwargs)
    if "usaurio" not in defaults:
        defaults["usaurio"] = create_django_contrib_auth_models_user()
    return Conta.objects.create(**defaults)


class FaturaViewTest(unittest.TestCase):
    '''
    Tests for Fatura
    '''
    def setUp(self):
        self.client = Client()

    def test_list_fatura(self):
        url = reverse('contas_fatura_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_fatura(self):
        url = reverse('contas_fatura_create')
        data = {
            "Descricao": "Descricao",
            "data_vencimento": "data_vencimento",
            "data_pagamento": "data_pagamento",
            "tipo_fatura": "tipo_fatura",
            "valor_fatura": "valor_fatura",
            "valor_pago": "valor_pago",
            "desconto": "desconto",
            "juro": "juro",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_fatura(self):
        fatura = create_fatura()
        url = reverse('contas_fatura_detail', args=[fatura.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_fatura(self):
        fatura = create_fatura()
        data = {
            "Descricao": "Descricao",
            "data_vencimento": "data_vencimento",
            "data_pagamento": "data_pagamento",
            "tipo_fatura": "tipo_fatura",
            "valor_fatura": "valor_fatura",
            "valor_pago": "valor_pago",
            "desconto": "desconto",
            "juro": "juro",
        }
        url = reverse('contas_fatura_update', args=[fatura.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ContaViewTest(unittest.TestCase):
    '''
    Tests for Conta
    '''
    def setUp(self):
        self.client = Client()

    def test_list_conta(self):
        url = reverse('contas_conta_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_conta(self):
        url = reverse('contas_conta_create')
        data = {
            "nome": "nome",
            "tipo_conta": "tipo_conta",
            "saldo_conta": "saldo_conta",
            "usaurio": create_django_contrib_auth_models_user().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_conta(self):
        conta = create_conta()
        url = reverse('contas_conta_detail', args=[conta.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_conta(self):
        conta = create_conta()
        data = {
            "nome": "nome",
            "tipo_conta": "tipo_conta",
            "saldo_conta": "saldo_conta",
            "usaurio": create_django_contrib_auth_models_user().pk,
        }
        url = reverse('contas_conta_update', args=[conta.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


