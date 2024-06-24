# middleware.py
from django.shortcuts import redirect

class RoleBasedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if 'usuario_id' in request.session:
                usuario_rol = request.session.get('usuario_rol', None)
                if usuario_rol == 'Administrador' and request.path != '/admin_dashboard/':
                    return redirect('admin_dashboard')
                elif usuario_rol == 'Usuario' and request.path != '/user_dashboard/':
                    return redirect('user_dashboard')
        return self.get_response(request)
