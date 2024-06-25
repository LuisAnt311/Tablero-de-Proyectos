from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/logout/') and 'usuario_id' in request.session:
            usuario_rol = request.session.get('usuario_rol')
            if (usuario_rol == 'Administrador' and not request.path.startswith('/admin_dashboard/') and
                not request.path.startswith('/agregar_proyecto/')):  # Excluir la URL de agregar proyecto
                return redirect(reverse('admin_dashboard'))
            elif (usuario_rol == 'Usuario' and not request.path.startswith('/user_dashboard/') and
                  not request.path.startswith('/agregar_proyecto/')):  # Excluir la URL de agregar proyecto
                return redirect(reverse('user_dashboard'))
        response = self.get_response(request)
        return response
