from django.urls import path, include
from django.views.generic import RedirectView  # <-- 1. Importas esto
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoViewSet, LoteStockViewSet, MermaViewSet, MovimientoViewSet,
    dashboard_web, productos_web
)

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'lotes', LoteStockViewSet)
router.register(r'mermas', MermaViewSet)
router.register(r'movimientos', MovimientoViewSet)

urlpatterns = [
    path('', dashboard_web, name='dashboard'),
    path('productos/', productos_web, name='productos_web'),
    
    # 2. Redirige la ruta vieja /productos/agregar/ de vuelta a /productos/
    path('productos/agregar/', RedirectView.as_view(url='/productos/', permanent=False)),

    path('api/v1/', include(router.urls)),
]