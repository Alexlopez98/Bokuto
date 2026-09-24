from rest_framework import serializers
from .models import Usuario, Categoria, Producto, LoteStock, Merma, Movimiento

# 1. Serializador de Categorías
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

# 2. Serializador de Productos
class ProductoSerializer(serializers.ModelSerializer):
    # Esto envía el nombre de la categoría al frontend (útil para mostrar en pantalla)
    # manteniendo el ID numérico en el campo 'categoria' para los envíos POST.
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = Producto
        fields = '__all__'

# 3. Serializador de Lotes
class LoteStockSerializer(serializers.ModelSerializer):
    # Esto envía el nombre del producto al frontend, no solo el código de barras
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')
    
    class Meta:
        model = LoteStock
        fields = '__all__'

# 4. Serializador de Mermas
class MermaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merma
        fields = '__all__'

# 5. Serializador de Movimientos
class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__'