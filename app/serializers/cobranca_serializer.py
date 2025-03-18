from rest_framework import serializers
from ..models import Cobranca


class CobrancaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cobranca
        fields = ['id', 'cliente', 'tipo', 'data_vencimento', 'valor', 'status',
                  'descricao', 'data_criacao', 'criado_por']
        read_only_fields = ['data_criacao', 'criado_por']

    def validate(self, data):
        """
        Validação customizada para os dados da cobrança
        """
        if data.get('valor', 0) <= 0:
            raise serializers.ValidationError(
                "O valor deve ser maior que zero")

        return data
