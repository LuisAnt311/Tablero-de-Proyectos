from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Rol, Usuario

@receiver(post_migrate)
def crear_roles_y_usuarios(sender, **kwargs):
    # Crear roles por defecto
    rol_administrador, _ = Rol.objects.get_or_create(
        nombre_rol='Administrador',
        descripcion_rol='Rol de administrador capaz de modificar cualquier cosa'
    )

    rol_usuario, _ = Rol.objects.get_or_create(
        nombre_rol='Usuario',
        descripcion_rol='Usuario común que trabaja'
    )

    # Crear usuarios por defecto asociados a cada rol
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        email='admin@admin.com'
    )
    admin_user.set_password('admin')
    admin_user.save()

    usuario_admin, _ = Usuario.objects.get_or_create(
        rol=rol_administrador,
        correo='admin@admin.com',
        nombre_usuario='admin',
        contrasena='admin'
    )

    user_user, _ = User.objects.get_or_create(
        username='user',
        email='user@user.com'
    )
    user_user.set_password('user')
    user_user.save()

    usuario_comun, _ = Usuario.objects.get_or_create(
        rol=rol_usuario,
        correo='user@user.com',
        nombre_usuario='user',
        contrasena='user'
    )
