from rest_framework import viewsets, status
from rest_framework.decorators import action
from ..filters.cobranca_filter import CobrancaFilter
from ..models.cobranca import Cobranca
from ..serializers import CobrancaSerializer, CriarCobrancasParceladasSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

parcelar_cobranca_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Mensagem de sucesso'),
        'cobrancas': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID da cobrança'),
                    'cliente': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID do cliente'),
                    'tipo': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo da cobrança'),
                    'data_vencimento': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Data de vencimento'),
                    'valor': openapi.Schema(type=openapi.TYPE_STRING, format='decimal', description='Valor da cobrança'),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status da cobrança'),
                    'descricao': openapi.Schema(type=openapi.TYPE_STRING, description='Descrição da cobrança'),
                    'data_criacao': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Data de criação'),
                },
            ),
            description='Lista de cobranças criadas'
        ),
    },
)


class CobrancaViewSet(viewsets.ModelViewSet):
    queryset = Cobranca.objects.all()
    serializer_class = CobrancaSerializer
    filterset_class = CobrancaFilter

    def perform_create(self, serializer):
        cobranca = serializer.save()
        cobranca.atualizar_status()  # Atualiza o status se estiver atrasada

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """
        Endpoint para cancelar uma cobrança
        """
        cobranca = self.get_object()
        if cobranca.status == 'PAGO':
            return Response({
                'error': 'Não é possível cancelar uma cobrança já paga'
            }, status=status.HTTP_400_BAD_REQUEST)

        cobranca.status = 'CANCELADO'
        cobranca.save()

        return Response({
            'message': 'Cobrança cancelada com sucesso'
        })

    @action(detail=False, methods=['get'])
    def atrasadas(self, request):
        """
        Lista todas as cobranças atrasadas
        """
        cobrancas = self.queryset.filter(status='ATRASADO')
        serializer = self.get_serializer(cobrancas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(
        # Define o serializer para o payload
        request_body=CriarCobrancasParceladasSerializer,
        # Define o serializer para a resposta
        responses={201: parcelar_cobranca_response_schema},
        operation_description="Endpoint para parcelar uma cobrança"
    )
    def parcelar_cobranca(self, request):
        """
        Endpoint para parcelar uma cobrança
        """
        serializer = CriarCobrancasParceladasSerializer(data=request.data)
        if serializer.is_valid():
            cobrancas = serializer.save()
            return Response({
                'message': f'Foram criadas {len(cobrancas)} cobranças parceladas com sucesso',
                'cobrancas': CobrancaSerializer(cobrancas, many=True).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
