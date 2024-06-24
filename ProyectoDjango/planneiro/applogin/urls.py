from django.urls import path
from . import views
from .views import agregar_rol,login_view

urlpatterns = [
    path('', views.mostrar_base_datos),
    #path('', admin.site.urls),
    path('mostrar-base-datos/', views.mostrar_base_datos, name='mostrar_base_datos'),
    path('agregar-rol/', views.agregar_rol, name='AgregarRol'),
    path('login/', login_view, name='login'),

]