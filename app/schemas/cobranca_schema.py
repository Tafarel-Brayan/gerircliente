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
