from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re

# Función validadora estricta para el RUT chileno (Formato: 1.111.111-1)
def validar_rut_estricto(value):
    patron = r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$'
    if not re.match(patron, value):
        raise ValidationError(
            'El RUT debe tener el formato estricto con puntos y guion. Ejemplo: 1.111.111-1'
        )

class Usuario(AbstractUser):
    # Opciones para el rol dentro del sistema logístico
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

    # Añadimos related_name para evitar conflictos con el modelo AbstractUser de Django
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_logistica_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_logistica_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.rol})"

class Producto(models.Model):
    codigo_barras = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class LoteStock(models.Model):
    UBICACION_CHOICES = (
        ('BODEGA', 'Bodega Principal'),
        ('SALA', 'Sala de Ventas'),
    )

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='lotes')
    cantidad = models.PositiveIntegerField()
    fecha_vencimiento = models.DateField()
    ubicacion = models.CharField(max_length=20, choices=UBICACION_CHOICES, default='BODEGA')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    operario_responsable = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Lote {self.producto.nombre} - Vence: {self.fecha_vencimiento}"