from rest_framework import serializers
from .models import Usuario, Producto, LoteStock, Merma, Movimiento

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class LoteStockSerializer(serializers.ModelSerializer):
    # Esto envía el nombre del producto al frontend, no solo el código de barras
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')
    
    class Meta:
        model = LoteStock
        fields = '__all__'

class MermaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merma
        fields = '__all__'

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__'