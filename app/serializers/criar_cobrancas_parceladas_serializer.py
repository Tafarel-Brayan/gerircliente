from rest_framework import serializers
from app.models.cobranca import Cobranca
from app.models.cliente import Cliente
from dateutil.relativedelta import relativedelta
from decimal import Decimal


class CriarCobrancasParceladasSerializer(serializers.Serializer):
    valor_da_cobranca = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal(1.00))
    parcelas = serializers.IntegerField(min_value=1)
    tipo_cobranca = serializers.CharField(max_length=50)
    data_vencimento = serializers.DateField()
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all())

    def create(self, validated_data):
        cliente = validated_data['cliente_id']
        valor_total = validated_data['valor_da_cobranca']
        parcelas = validated_data['parcelas']
        tipo_cobranca = validated_data['tipo_cobranca']
        data_vencimento = validated_data['data_vencimento']

        valor_parcela = valor_total / parcelas
        cobrancas = []

        for i in range(parcelas):
            vencimento_parcela = data_vencimento + relativedelta(months=i)
            cobranca = Cobranca(
                cliente=cliente,
                data_vencimento=vencimento_parcela,
                valor=valor_parcela,
                descricao=f"{tipo_cobranca} - Parcela {i + 1}/{parcelas}"
            )
            cobrancas.append(cobranca)

        # Salva todas as cobranças no banco de dados
        Cobranca.objects.bulk_create(cobrancas)
        return cobrancas
