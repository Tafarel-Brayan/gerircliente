from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, CobrancaViewSet, PagamentoViewSet

# Inicializa o router
router = DefaultRouter()

# Registra Rotas
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'cobrancas', CobrancaViewSet, basename='cobranca')
router.register(r'pagamentos', PagamentoViewSet, basename='pagamento')

urlpatterns = router.urls
