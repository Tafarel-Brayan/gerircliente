from rest_framework import serializers
from ..models import Cobranca


class CobrancaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cobranca
        fields = ['id', 'cliente', 'data_vencimento', 'valor', 'status',
                  'descricao', 'data_criacao']
        read_only_fields = ['data_criacao']

    def validate(self, data):
        """
        Validação customizada para os dados da cobrança
        """
        if data.get('valor', 0) <= 0:
            raise serializers.ValidationError(
                "O valor deve ser maior que zero")

        return data
