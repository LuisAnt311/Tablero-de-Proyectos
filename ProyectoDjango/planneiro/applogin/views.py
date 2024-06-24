from django.http import HttpResponse
from .models import Rol, Usuario, Proyecto, Impacto, RecursoMaterial, RecursoHumano, Documento, Fase, Riesgo
from .forms import FaseForm, RolForm, LoginForm
from django.shortcuts import render,redirect
# Create your views here.

def hello(request):
    return HttpResponse("Hola mundo")

def mostrar_base_datos(request):
    roles = Rol.objects.all()
    usuarios = Usuario.objects.all()
    proyectos = Proyecto.objects.all()
    impactos = Impacto.objects.all()
    recursos_materiales = RecursoMaterial.objects.all()
    recursos_humanos = RecursoHumano.objects.all()
    documentos = Documento.objects.all()
    fases = Fase.objects.all()
    riesgos = Riesgo.objects.all()

    context = {
        'roles': roles,
        'usuarios': usuarios,
        'proyectos': proyectos,
        'impactos': impactos,
        'recursos_materiales': recursos_materiales,
        'recursos_humanos': recursos_humanos,
        'documentos': documentos,
        'fases': fases,
        'riesgos': riesgos,
    }
    return render(request, 'applogin/mostrar_base_datos.html', context)

def agregar_rol(request):
    if request.method == 'POST':
        rol_form = RolForm(request.POST)
        if rol_form.is_valid():
            rol_form.save()  # Guardar el formulario si es válido
            return redirect('mostrar_base_datos')  # Redirigir a una página de éxito o a la lista de roles
    else:
        rol_form = RolForm()  # Crear una instancia de RolForm vacía para mostrar el formulario

    return render(request, 'applogin/AgregarRol.html', {'rol_form': rol_form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                usuario = Usuario.objects.get(correo=email)
                if password == usuario.contrasena:
                    # Simular el login de Django
                    request.session['usuario_id'] = usuario.id
                    request.session['usuario_rol'] = usuario.rol.nombre_rol
                    if usuario.rol.nombre_rol == 'Administrador':
                        return redirect('admin_dashboard')
                    else:
                        return redirect('user_dashboard')
                else:
                    form.add_error('password', 'Contraseña incorrecta')
            except Usuario.DoesNotExist:
                form.add_error('email', 'Correo electrónico no registrado')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})