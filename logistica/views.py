from rest_framework import viewsets
from .models import Producto, LoteStock, Merma, Movimiento
from django.shortcuts import render
from .serializers import (
    ProductoSerializer, 
    LoteStockSerializer, 
    MermaSerializer, 
    MovimientoSerializer
)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class LoteStockViewSet(viewsets.ModelViewSet):
    queryset = LoteStock.objects.all()
    serializer_class = LoteStockSerializer
    # Ordenamiento FEFO por defecto: los próximos a vencer salen primero
    ordering = ['fecha_vencimiento']

class MermaViewSet(viewsets.ModelViewSet):
    queryset = Merma.objects.all()
    serializer_class = MermaSerializer

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    
def dashboard_web(request):
    return render(request, 'dashboard.html')

def productos_web(request):
    return render(request, 'productos.html')