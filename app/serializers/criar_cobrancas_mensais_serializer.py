from rest_framework import serializers
from ..models.cliente import Cliente
from decimal import Decimal


class CriarCobrancasMensaisSerializer(serializers.Serializer):
    cliente = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all())
    valor = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantidade_meses = serializers.IntegerField(
        min_value=Decimal(1), max_value=12)
    dia_vencimento = serializers.IntegerField(
        min_value=Decimal(1), max_value=31)
    descricao_base = serializers.CharField(max_length=200)
