from django.http import HttpResponse
from .models import Rol, Usuario, Proyecto, Impacto, RecursoMaterial, RecursoHumano, Documento, Fase, Riesgo,RelacionDocumento
from .forms import RelacionarDocumentoForm, RolForm, LoginForm,ProyectoForm,UsuarioForm,AsignarRecursoHumanoForm, AgregarRecursoMaterialForm, AgregarDocumentoForm, AgregarRiesgoForm, AgregarFaseForm,ProyectoEditarForm,InsertarUsuarioForm
from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST,require_GET
from django.contrib.auth.decorators import login_required
from .forms import ProyectoForm
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import InsertarUsuarioForm
# Create your views here.

def hello(request):
    return HttpResponse("Hola mundo")
def mi_vista(request):
    return render(request, 'applogin/index.html')

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
                        return redirect('admin_dashboard')
                else:
                    form.add_error('password', 'Contraseña incorrecta')
            except Usuario.DoesNotExist:
                form.add_error('email', 'Correo electrónico no registrado')
    else:
        form = LoginForm()

    return render(request, 'applogin/login.html', {'form': form})

from django.db.models import Q

def admin_dashboard(request):
    if request.session.get('usuario_rol') != 'Administrador':
        return redirect('login')  # Redireccionar si el usuario no es administrador

    usuarios = Usuario.objects.all()
    proyectos = Proyecto.objects.all().order_by('id')  # Ordenar proyectos por ID

    # Obtener el término de búsqueda del parámetro GET 'q'
    query = request.GET.get('q')
    if query:
        # Filtrar proyectos por nombre_proyecto, estado y admin_proyecto_usuario__nombre_usuario
        proyectos = proyectos.filter(
            Q(nombre_proyecto__icontains=query) |
            Q(estado__icontains=query) |
            Q(admin_proyecto_usuario__nombre_usuario__icontains=query)
        )

    # Paginación
    paginator = Paginator(proyectos, 5)  # Mostrar 5 proyectos por página
    page = request.GET.get('page')
    try:
        proyectos_paginados = paginator.page(page)
    except PageNotAnInteger:
        proyectos_paginados = paginator.page(1)
    except EmptyPage:
        proyectos_paginados = paginator.page(paginator.num_pages)

    contexto = {
        'usuario_nombre': request.session.get('usuario_nombre'),
        'usuario_rol': request.session.get('usuario_rol'),
        'usuarios': usuarios,
        'proyectos': proyectos_paginados,  # Cambiar a proyectos paginados
        'form': ProyectoForm(),  # Incluir formulario de proyecto en el contexto
        'form_usuario': InsertarUsuarioForm(),  # Incluir formulario de usuario en el contexto
    }
    return render(request, 'MenusAdmins/admin_dashboard.html', contexto)


def insertar_usuario(request):
    if request.method == 'POST':
        form = InsertarUsuarioForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            usuario_existente = Usuario.objects.filter(correo=correo).first()
            if usuario_existente:
                # Actualizar usuario existente
                usuario_existente.rol = form.cleaned_data['rol']
                usuario_existente.nombre_usuario = form.cleaned_data['nombre_usuario']
                usuario_existente.contrasena = form.cleaned_data['contrasena']
                usuario_existente.save()
                return HttpResponse("Usuario actualizado correctamente.")
            else:
                # Insertar nuevo usuario
                form.save()
                return HttpResponse("Usuario insertado correctamente.")
        else:
            return HttpResponse(f"Formulario inválido: {form.errors}")
    return HttpResponse("Solicitud no válida.")

from .forms import AgregarDocumentoFormProyecto,RelacionarDocumentoForm
def user_dashboard(request):
    if request.session.get('usuario_rol') != 'Usuario':
        return redirect('login')  # Redireccionar si el usuario no es usuario normal

    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(pk=usuario_id)

    # Obtener todos los proyectos en los que el usuario es recurso humano
    proyectos = Proyecto.objects.filter(recursos_humanos__usuario=usuario)

    # Implementar búsqueda por nombre de proyecto
    query = request.GET.get('q')
    if query:
        proyectos = proyectos.filter(
            Q(nombre_proyecto__icontains=query)
        )

    # Si se envía el formulario para agregar documento
    if request.method == 'POST':
        form = AgregarDocumentoFormProyecto(usuario, request.POST)
        if form.is_valid():
            documento = form.save()
            return redirect('user_dashboard')
        elif 'submit_relacion' in request.POST:
            form_relacion = RelacionarDocumentoForm(request.POST)
            if form_relacion.is_valid():
                form_relacion.save()
                return redirect('user_dashboard')  # Redireccionar después de guardar el documento
    else:
        form = AgregarDocumentoFormProyecto(usuario)
        form_relacion = RelacionarDocumentoForm()


    contexto = {
        'usuario_nombre': request.session.get('usuario_nombre'),
        'usuario_rol': request.session.get('usuario_rol'),
        'proyectos': proyectos,
        'form': form,
        'form_relacion': form_relacion  # Pasar el formulario al contexto
    }
    return render(request, 'MenusUsuarios/user_dashboard.html', contexto)

def agregar_documento_usuario(request, proyecto_id):
    proyecto = Proyecto.objects.get(pk=proyecto_id)
    if request.method == 'POST':
        form = AgregarDocumentoFormProyecto(request.POST, usuario=request.user)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.proyecto = proyecto
            documento.save()
            return redirect('user_dashboard')  # Redireccionar después de guardar el documento
    else:
        form = AgregarDocumentoFormProyecto(usuario=request.user)

    contexto = {
        'form': form,
        'proyecto': proyecto,
    }

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
            return redirect('login')  # Devuelve una respuesta JSON indicando éxito
        else:
            errors = form.errors.as_json()
            return redirect('login')  # Devuelve errores en JSON con estado 400 (Bad Request)
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
from .forms import AgregarRecursoMaterialForm, AsignarRecursoHumanoForm, AgregarDocumentoForm, AgregarRiesgoForm, AgregarFaseForm
def detalles_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    impactos = Impacto.objects.filter(proyecto=proyecto)
    recursos_materiales = RecursoMaterial.objects.filter(proyecto=proyecto)
    recursos_humanos = RecursoHumano.objects.filter(proyecto=proyecto)
    documentos = Documento.objects.filter(proyecto=proyecto)
    fases = Fase.objects.filter(proyecto=proyecto)
    riesgos = Riesgo.objects.filter(proyecto=proyecto)
    relaciones_documento = RelacionDocumento.objects.filter(fase__proyecto=proyecto).select_related('documento', 'fase')
    # Inicialización de los formularios con el contexto del proyecto
    agregar_recurso_material_form = AgregarRecursoMaterialForm(proyecto, request.POST or None)
    asignar_recurso_humano_form = AsignarRecursoHumanoForm(proyecto, request.POST or None)
    agregar_documento_form = AgregarDocumentoForm(proyecto, request.POST or None)
    agregar_riesgo_form = AgregarRiesgoForm(proyecto, request.POST or None)
    agregar_fase_form = AgregarFaseForm(proyecto, request.POST or None)
    editar_proyecto_form = ProyectoEditarForm(instance=proyecto)

    contexto = {
        'proyecto': proyecto,
        'impactos': impactos,
        'recursos_materiales': recursos_materiales,
        'recursos_humanos': recursos_humanos,
        'documentos': documentos,
        'fases': fases,
        'relaciones_documento': relaciones_documento,
        'riesgos': riesgos,
        'agregar_recurso_material_form': agregar_recurso_material_form,
        'asignar_recurso_humano_form': asignar_recurso_humano_form,
        'agregar_documento_form': agregar_documento_form,
        'agregar_riesgo_form': agregar_riesgo_form,
        'agregar_fase_form': agregar_fase_form,
        'form': editar_proyecto_form,
    }

    return render(request, 'MenusAdmins/detallesproyecto.html', contexto)

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el formulario si es válido
            return redirect('inicio')  # Redireccionar a la página de inicio u otra página deseada después de guardar
    else:
        form = UsuarioForm()

    return render(request, 'MenusAdmins/Modales/AddRecursoHumano.html', {'form': form})

def asignar_recurso_humano(request, proyecto_id):
    print(f"Proyecto ID: {proyecto_id}")  # Debugging
    
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = AsignarRecursoHumanoForm(proyecto, request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('detalles_proyecto', proyecto_id=proyecto_id)
            except ValidationError as e:
                print(f"Validation Error: {e.message}")  # Debugging
                form.add_error('usuario', e.message)
        else:
            print("Formulario no válido")  # Debugging
    else:
        form = AsignarRecursoHumanoForm(proyecto)
    
    return render(request, 'MenusAdmins/detallesproyecto.html', {'form': form, 'proyecto_id': proyecto_id})


def agregar_recurso_material(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = AgregarRecursoMaterialForm(proyecto, request.POST)
        if form.is_valid():
            form.save()
            return redirect('detalles_proyecto', proyecto_id=proyecto_id)
    else:
        form = AgregarRecursoMaterialForm(proyecto)
    
    return render(request, 'MenusAdmins/detallesproyecto.html', {'form': form})

def agregar_documento(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = AgregarDocumentoForm(proyecto, request.POST)
        if form.is_valid():
            form.save()
            return redirect('detalles_proyecto', proyecto_id=proyecto_id)
    else:
        form = AgregarDocumentoForm(proyecto)
    
    return render(request, 'MenusAdmins/detallesproyecto.html', {'form': form})

def agregar_riesgo(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = AgregarRiesgoForm(proyecto, request.POST)
        if form.is_valid():
            form.save()
            return redirect('detalles_proyecto', proyecto_id=proyecto_id)
    else:
        form = AgregarRiesgoForm(proyecto)
    
    return render(request, 'MenusAdmins/detallesproyecto.html', {'form': form})

def agregar_fase(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        form = AgregarFaseForm(proyecto, request.POST)
        if form.is_valid():
            form.save()
            return redirect('detalles_proyecto', proyecto_id=proyecto_id)
    else:
        form = AgregarFaseForm(proyecto)
    
    return render(request, 'MenusAdmins/detallesproyecto.html', {'form': form})

def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    if request.method == 'POST':
        form = ProyectoEditarForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('detalles_proyecto', proyecto_id=proyecto_id)
    else:
        form = ProyectoEditarForm(instance=proyecto)
    
    context = {
        'form': form,
        'proyecto': proyecto,
    }
    return render(request, 'MenusAdmins/editarproyecto.html', context)

def relacionar_documento(request):
    if request.method == 'POST':
        form = RelacionarDocumentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = RelacionarDocumentoForm()
    return render(request, 'relacionar_documento.html', {'form': form})