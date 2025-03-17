from ..models import Cobranca
from django_filters import rest_framework as filters

class CobrancaFilter(filters.FilterSet):
    data_vencimento_inicio = filters.DateFilter(field_name='data_vencimento', lookup_expr='gte')
    data_vencimento_fim = filters.DateFilter(field_name='data_vencimento', lookup_expr='lte')
    
    class Meta:
        model = Cobranca
        fields = {
            'cliente': ['exact'],
            'status': ['exact'],
            'valor': ['gte', 'lte'],
        }
