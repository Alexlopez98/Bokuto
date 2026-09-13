from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, LoteStockViewSet, MermaViewSet, MovimientoViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'lotes', LoteStockViewSet)
router.register(r'mermas', MermaViewSet)
router.register(r'movimientos', MovimientoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]