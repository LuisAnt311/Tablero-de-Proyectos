from django.urls import path
from . import views
from .views import agregar_rol,login_view,admin_dashboard, user_dashboard,logout_view,agregar_proyecto,detalles_proyecto,insertar_usuario,mi_vista

urlpatterns = [
    path('', views.mi_vista, name='mostrar_base_datos'),
    path('mostrar-base-datos/', views.mostrar_base_datos, name='mostrar_base_datos'),
    path('agregar-rol/', views.agregar_rol, name='agregar_rol'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/detalles-proyecto/<int:proyecto_id>/', views.detalles_proyecto, name='detalles_proyecto'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('agregar_proyecto/', views.agregar_proyecto, name='agregar_proyecto'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),

    path('relacionar_documentousuario/', views.relacionar_documento, name='relacionar_documento'),
    path('agregar_documentousuario/<int:proyecto_id>/', views.agregar_documento_usuario, name='agregar_documentousuario'),

   path('insertar_usuario/', views.insertar_usuario, name='insertar_usuario'),

    path('proyecto/<int:proyecto_id>/agregar-fase/', views.agregar_fase, name='agregar_fase'),
    path('proyecto/<int:proyecto_id>/asignar-recurso-humano/', views.asignar_recurso_humano, name='asignar_recurso_humano'),
    path('proyecto/<int:proyecto_id>/agregar-recurso-material/', views.agregar_recurso_material, name='agregar_recurso_material'),
    path('proyecto/<int:proyecto_id>/agregar-documento/', views.agregar_documento, name='agregar_documento'),
    path('proyecto/<int:proyecto_id>/agregar-riesgo/', views.agregar_riesgo, name='agregar_riesgo'),
    path('editar_proyecto/<int:proyecto_id>/', views.editar_proyecto, name='editar_proyecto'),
]