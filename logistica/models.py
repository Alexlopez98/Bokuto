from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re

# 1. Validador estricto de RUT
def validar_rut_estricto(value):
    patron = r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$'
    if not re.match(patron, value):
        raise ValidationError(
            'El RUT debe tener el formato estricto con puntos y guion. Ejemplo: 1.111.111-1'
        )

# 2. Usuarios y Roles
class Usuario(AbstractUser):
    ROL_CHOICES = (
        ('BODEGUERO', 'Bodeguero'),
        ('OPERADOR_SALA', 'Operador de Sala'),
        ('ADMINISTRADOR', 'Administrador'),
    )

    rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[validar_rut_estricto],
        help_text="RUT con formato estricto: 1.111.111-1"
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='OPERADOR_SALA')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_logistica_set',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_logistica_set',
        blank=True,
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.rol})"


# 3. Categorías para Productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


# 4. Catálogo Maestro de Productos
class Producto(models.Model):
    codigo_barras = models.CharField(max_length=50, primary_key=True)
    codigo_interno = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    nombre = models.CharField(max_length=150)
    marca = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    
    # Relación de Llave Foránea hacia la tabla Categoria
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    
    stock_minimo = models.PositiveIntegerField(default=10, help_text="Umbral para alerta en panel admin")
    
    # Campo para la imagen de referencia (preparado para AWS S3)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True, help_text="Imagen de referencia del producto")

    def __str__(self):
        return f"{self.nombre} ({self.marca}) - {self.codigo_barras}"

# 5. Control FEFO: Lotes de Stock
class LoteStock(models.Model):
    UBICACION_CHOICES = (
        ('BODEGA', 'Bodega Principal'),
        ('SALA', 'Sala de Ventas'),
    )
    ESTADO_CHOICES = (
        ('ACTIVO', 'Activo'),
        ('AGOTADO', 'Agotado'),
        ('VENCIDO', 'Vencido'),
    )

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='lotes')
    cantidad_inicial = models.PositiveIntegerField(help_text="Stock con el que ingresó el lote")
    cantidad_actual = models.PositiveIntegerField(help_text="Stock disponible real")
    fecha_vencimiento = models.DateField(db_index=True)
    ubicacion = models.CharField(max_length=20, choices=UBICACION_CHOICES, default='BODEGA')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    operario_responsable = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Lote {self.id} | {self.producto.nombre} | Vence: {self.fecha_vencimiento}"

# 6. Auditoría: Mermas
class Merma(models.Model):
    MOTIVO_CHOICES = (
        ('VENCIMIENTO', 'Vencimiento'),
        ('ROTURA', 'Rotura o Daño'),
        ('ROBO', 'Robo o Extravío'),
        ('ERROR_INVENTARIO', 'Ajuste por Error de Inventario'),
    )

    lote = models.ForeignKey(LoteStock, on_delete=models.CASCADE, related_name='mermas')
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(max_length=30, choices=MOTIVO_CHOICES)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    operario_responsable = models.ForeignKey(Usuario, on_delete=models.PROTECT)

    def __str__(self):
        return f"Merma: {self.cantidad} unid. de {self.lote.producto.nombre} ({self.motivo})"

# 7. Movimientos Logísticos (Tracking)
class Movimiento(models.Model):
    lote = models.ForeignKey(LoteStock, on_delete=models.CASCADE, related_name='movimientos')
    cantidad = models.PositiveIntegerField()
    origen = models.CharField(max_length=50, help_text="Ej: Bodega Central")
    destino = models.CharField(max_length=50, help_text="Ej: Pasillo 4")
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    operario_responsable = models.ForeignKey(Usuario, on_delete=models.PROTECT)

    def __str__(self):
        return f"Movimiento: {self.cantidad} unid. de {self.origen} a {self.destino}"