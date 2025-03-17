from rest_framework import viewsets
from ..models.cliente import Cliente
from ..serializers.cliente_serializer import ClienteSerializer
from rest_framework.permissions import IsAuthenticated


class ClienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite operações CRUD em Clientes.

    list:
    Retorna uma lista de todos os clientes cadastrados.

    create:
    Cria um novo cliente.

    retrieve:
    Retorna os detalhes de um cliente específico.

    update:
    Atualiza todos os campos de um cliente.

    partial_update:
    Atualiza parcialmente os campos de um cliente.

    destroy:
    Remove um cliente.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    # Apenas usuários autenticados podem acessar
    permission_classes = [IsAuthenticated]
