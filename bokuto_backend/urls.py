from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conectamos toda la API de logistica bajo la ruta api/v1/
    path('api/v1/', include('logistica.urls')),
]