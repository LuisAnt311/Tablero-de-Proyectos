from django.contrib import admin
from django.urls import path, include
from applogin.views import hello

urlpatterns = [
    path('', include('applogin.urls')),  # Ruta corregida
    path('admin/', admin.site.urls),
    
]
