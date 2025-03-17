"""
Este módulo contém a definição da viewset para o modelo Pagamento.
"""

from rest_framework import viewsets
from ..models.pagamento import Pagamento
from ..serializers import PagamentoSerializer


class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
