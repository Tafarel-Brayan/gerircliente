from rest_framework import viewsets, status
from rest_framework.decorators import action
from ..filters.cobranca_filter import CobrancaFilter
from ..models.cobranca import Cobranca
from ..serializers import CobrancaSerializer, CriarCobrancasMensaisSerializer
from rest_framework.response import Response


class CobrancaViewSet(viewsets.ModelViewSet):
    queryset = Cobranca.objects.all()
    serializer_class = CobrancaSerializer
    filterset_class = CobrancaFilter

    def perform_create(self, serializer):
        cobranca = serializer.save()
        cobranca.atualizar_status()  # Atualiza o status se estiver atrasada

    @action(detail=False, methods=['post'])
    def criar_mensais(self, request):
        """
        Endpoint para criar cobranças mensais
        """
        serializer = CriarCobrancasMensaisSerializer(data=request.data)
        if serializer.is_valid():
            try:
                cobrancas = Cobranca.criar_cobrancas_mensais(
                    cliente=serializer.validated_data['cliente'],
                    valor=serializer.validated_data['valor'],
                    quantidade_meses=serializer.validated_data['quantidade_meses'],
                    dia_vencimento=serializer.validated_data['dia_vencimento'],
                    descricao_base=serializer.validated_data['descricao_base']
                )

                return Response({
                    'message': f'Foram criadas {len(cobrancas)} cobranças com sucesso',
                    'cobrancas': CobrancaSerializer(cobrancas, many=True).data
                }, status=status.HTTP_201_CREATED)

            except ValueError as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
