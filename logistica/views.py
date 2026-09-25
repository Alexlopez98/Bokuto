from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Categoria, Producto, LoteStock, Merma, Movimiento
from .serializers import (
    CategoriaSerializer,
    ProductoSerializer, 
    LoteStockSerializer, 
    MermaSerializer, 
    MovimientoSerializer
)

# 1. Importamos los permisos de la API (DRF)
from .permissions import IsBodeguero, IsOperadorSala, IsAdministrador

# 2. Funciones validadoras para proteger las vistas web (HTML)
def es_administrador(user):
    return user.is_authenticated and user.groups.filter(name='Administrador').exists()

def es_bodeguero_o_admin(user):
    return user.is_authenticated and user.groups.filter(name__in=['Bodeguero', 'Administrador']).exists()


# ==========================================
# ENDPOINTS DE LA API (DRF)
# ==========================================

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    # Solo usuarios logueados pueden ver/crear categorías
    permission_classes = [IsAdministrador] 

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    # El Bodeguero (para buscar inventario) y el Admin tienen acceso
    # Usamos el operador "|" (OR) para combinar permisos
    permission_classes = [IsBodeguero | IsAdministrador]

class LoteStockViewSet(viewsets.ModelViewSet):
    queryset = LoteStock.objects.all()
    serializer_class = LoteStockSerializer
    ordering = ['fecha_vencimiento']
    # Bodeguero controla el stock y caducidad, Admin supervisa
    permission_classes = [IsBodeguero | IsAdministrador]

class MermaViewSet(viewsets.ModelViewSet):
    queryset = Merma.objects.all()
    serializer_class = MermaSerializer
    # ¡EL BLINDAJE PARA JOHAN! Solo el Operador de Sala registra mermas
    permission_classes = [IsOperadorSala | IsAdministrador]

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    # Los movimientos (auditoría) son exclusivos del Administrador
    permission_classes = [IsAdministrador]
    

# ==========================================
# VISTAS WEB CLÁSICAS (HTML)
# ==========================================

@login_required(login_url='/login/') # Redirige al login si no tiene sesión
@user_passes_test(es_administrador, login_url='/login/') # Corta el paso si no es Admin
def dashboard_web(request):
    return render(request, 'dashboard.html')

@login_required(login_url='/login/')
@user_passes_test(es_bodeguero_o_admin, login_url='/login/')
def productos_web(request):
    return render(request, 'productos.html')