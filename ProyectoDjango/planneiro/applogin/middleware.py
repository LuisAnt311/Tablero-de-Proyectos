from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/logout/') and 'usuario_id' in request.session:
            usuario_rol = request.session.get('usuario_rol')
            if (usuario_rol == 'Administrador' and not request.path.startswith('/admin_dashboard/') and
                not request.path.startswith('/agregar_proyecto/') and
                not request.path.startswith('/proyecto/') and
                not request.path.startswith('/insertar_usuario/') and
                not request.path.startswith('/editar_proyecto/')):
                return redirect(reverse('admin_dashboard'))
            elif (usuario_rol == 'Usuario' and not request.path.startswith('/user_dashboard/') and
                  not request.path.startswith('/agregar_proyecto/') and
                  not request.path.startswith('/proyecto/') and
                  not request.path.startswith('/proyecto/') and
                  not request.path.startswith('/relacionar_documentousuario/') and
               
                  not request.path.startswith('/insertar_usuario/') and
                  not request.path.startswith('/proyecto/<int:proyecto_id>/agregar-recurso-material/')):
                
                return redirect(reverse('user_dashboard'))
        response = self.get_response(request)
        return response