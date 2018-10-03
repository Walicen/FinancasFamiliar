from . import models
from . import serializers
from rest_framework import viewsets, permissions


class FaturaViewSet(viewsets.ModelViewSet):
    """ViewSet for the Fatura class"""

    queryset = models.Fatura.objects.all()
    serializer_class = serializers.FaturaSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContaViewSet(viewsets.ModelViewSet):
    """ViewSet for the Conta class"""

    queryset = models.Conta.objects.all()
    serializer_class = serializers.ContaSerializer
    permission_classes = [permissions.IsAuthenticated]


