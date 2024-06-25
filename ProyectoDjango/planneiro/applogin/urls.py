from django.urls import path
from . import views
from .views import agregar_rol,login_view,admin_dashboard, user_dashboard,logout_view,agregar_proyecto

urlpatterns = [
    path('', views.mostrar_base_datos, name='mostrar_base_datos'),
    path('mostrar-base-datos/', views.mostrar_base_datos, name='mostrar_base_datos'),
    path('agregar-rol/', views.agregar_rol, name='agregar_rol'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('agregar_proyecto/', views.agregar_proyecto, name='agregar_proyecto'),
]