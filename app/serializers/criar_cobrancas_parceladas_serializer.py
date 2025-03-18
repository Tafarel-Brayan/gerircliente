from rest_framework import serializers
from app.models.cobranca import Cobranca
from app.models.cliente import Cliente
from dateutil.relativedelta import relativedelta
from decimal import Decimal
import datetime


class CriarCobrancasParceladasSerializer(serializers.Serializer):
    valor_da_cobranca = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal(1.00))
    parcelas = serializers.IntegerField(min_value=1)
    tipo_cobranca = serializers.CharField(max_length=50)
    data_vencimento = serializers.DateField()
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all())

    def validate_valor_da_cobranca(self, value):
        """Valida se o valor da cobrança é maior ou igual a 150 reais."""
        if value < Decimal('150.00'):
            raise serializers.ValidationError(
                "O valor da cobrança deve ser maior ou igual a 150 reais.")
        return value

    def validate_parcelas(self, value):
        """Valida se a quantidade de parcelas é maior ou igual a 2."""
        if value < 2:
            raise serializers.ValidationError(
                "A quantidade de parcelas deve ser no mínimo 2.")
        return value

    def validate_data_vencimento(self, value):
        """Valida e ajusta a data de vencimento para o próximo dia útil se for um domingo."""
        if value.weekday() == 6:  # 6 representa domingo
            value += datetime.timedelta(days=1)  # Ajusta para segunda-feira
        return value

    def create(self, validated_data):
        request = self.context.get('request')  # Obter o request do contexto
        usuario = request.user if request else None  # Obter o usuário autenticado

        cliente = validated_data['cliente_id']
        valor_total = validated_data['valor_da_cobranca']
        parcelas = validated_data['parcelas']
        tipo_cobranca = validated_data['tipo_cobranca']
        data_vencimento = validated_data['data_vencimento']

        # Verifica se o valor é menor que 150 reais
        if valor_total < Decimal('150.00'):
            # Cria uma única cobrança
            cobranca = Cobranca.objects.create(
                cliente=cliente,
                data_vencimento=data_vencimento,
                valor=valor_total,
                descricao=f"{tipo_cobranca} - Cobrança única",
                criado_por=usuario
            )
            return [cobranca]  # Retorna uma lista com a única cobrança

        # Caso contrário, cria as parcelas

        valor_parcela = valor_total / parcelas
        cobrancas = []

        for i in range(parcelas):
            vencimento_parcela = data_vencimento + relativedelta(months=i)
            cobranca = Cobranca(
                cliente=cliente,
                data_vencimento=vencimento_parcela,
                valor=valor_parcela,
                descricao=f"{tipo_cobranca} - Parcela {i + 1}/{parcelas}",
                criado_por=usuario
            )
            cobrancas.append(cobranca)

        # Salva todas as cobranças no banco de dados
        Cobranca.objects.bulk_create(cobrancas)
        return cobrancas
