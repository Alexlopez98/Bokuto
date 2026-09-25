from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Categoria, Producto, LoteStock, Merma, Movimiento

# 1. Registrar el Modelo de Usuario Personalizado
Usuario = get_user_model()
admin.site.register(Usuario, UserAdmin)

# 2. Registrar los Modelos del Negocio
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(LoteStock)
admin.site.register(Merma)
admin.site.register(Movimiento)