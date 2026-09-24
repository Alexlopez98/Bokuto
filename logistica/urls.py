from django.urls import path, include
from django.views.generic import RedirectView 
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet,
    ProductoViewSet, 
    LoteStockViewSet, 
    MermaViewSet, 
    MovimientoViewSet,
    dashboard_web, 
    productos_web
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'lotes', LoteStockViewSet)
router.register(r'mermas', MermaViewSet)
router.register(r'movimientos', MovimientoViewSet)

urlpatterns = [
    path('', dashboard_web, name='dashboard'),
    path('productos/', productos_web, name='productos_web'),
    
    path('productos/agregar/', RedirectView.as_view(url='/productos/', permanent=False)),

    path('api/v1/', include(router.urls)),
]