from django.http import HttpResponse
from .models import Rol, Usuario, Proyecto, Impacto, RecursoMaterial, RecursoHumano, Documento, Fase, Riesgo
from .forms import FaseForm, RolForm, LoginForm,ProyectoForm
from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST,require_GET
from django.contrib.auth.decorators import login_required
from .forms import ProyectoForm
from django.http import JsonResponse
from django.urls import reverse
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
                    # Autenticación exitosa
                    request.session['usuario_id'] = usuario.id
                    request.session['usuario_nombre'] = usuario.nombre_usuario
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

    return render(request, 'applogin/login.html', {'form': form})


def admin_dashboard(request):
    if request.session.get('usuario_rol') != 'Administrador':
        return redirect('login')  # Redireccionar si el usuario no es administrador
    
    usuarios = Usuario.objects.all()
    proyectos = Proyecto.objects.all()  # Asegúrate de obtener los proyectos
    form = ProyectoForm()  # Crear una instancia del formulario

    contexto = {
        'usuario_nombre': request.session.get('usuario_nombre'),
        'usuario_rol': request.session.get('usuario_rol'),
        'usuarios': usuarios,
        'proyectos': proyectos,  # Añadir los proyectos al contexto
        'form': form,  # Añadir el formulario al contexto
    }
    return render(request, 'MenusAdmins/admin_dashboard.html', contexto)


def user_dashboard(request):
    if request.session.get('usuario_rol') != 'Usuario':
        return redirect('login')  # Redireccionar si el usuario no es usuario normal

    contexto = {
        'usuario_nombre': request.session.get('usuario_nombre'),
        'usuario_rol': request.session.get('usuario_rol'),
    }
    return render(request, 'MenusUsuarios/user_dashboard.html', contexto)


@require_GET
def logout_view(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    if 'usuario_nombre' in request.session:
        del request.session['usuario_nombre']
    if 'usuario_rol' in request.session:
        del request.session['usuario_rol']
    return redirect('login')

def agregar_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Bien'})  # Devuelve una respuesta JSON indicando éxito
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)  # Devuelve errores en JSON con estado 400 (Bad Request)
    else:
        form = ProyectoForm()

    usuarios = Usuario.objects.all()
    proyectos = Proyecto.objects.all()

    context = {
        'form': form,
        'usuarios': usuarios,
        'proyectos': proyectos,
    }
    return render(request, 'MenusAdmins/admin_dashboard.html', context) # Imprimir errores del formulario para depuración