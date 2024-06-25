from django import forms
from .models import Fase, Rol,Proyecto,Usuario,RecursoHumano,RecursoMaterial,Documento,Riesgo
from django.core.exceptions import ValidationError 

class FaseForm(forms.ModelForm):
    class Meta:
        model = Fase
        fields = ['proyecto', 'fase', 'concluido']

#Form para agregar roles
class RolForm(forms.ModelForm):
    class Meta:
        model = Rol  # Especifica el modelo al que pertenece este formulario
        fields = ['nombre_rol', 'descripcion_rol']
        labels = {
            'nombre_rol': 'Nombre del Rol',
            'descripcion_rol': 'Descripción del Rol',
        }
        widgets = {
            'nombre_rol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del rol'}),
            'descripcion_rol': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese la descripción del rol'}),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo electrónico'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}))
class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre_proyecto', 'admin_proyecto_usuario', 'estado', 'porcentaje', 'fecha_inicio', 'fecha_final', 'presupuesto', 'costo_final', 'descripcion']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_final': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nombre_proyecto': forms.TextInput(attrs={'class': 'form-control'}),
            'admin_proyecto_usuario': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('Pendiente', 'Pendiente'),
                ('En proceso', 'En proceso'),
                ('Finalizado', 'Finalizado'),
            ]),
            'porcentaje': forms.NumberInput(attrs={'class': 'form-control'}),
            'presupuesto': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_final': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),  # Widget para el campo de descripción
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_final = cleaned_data.get('fecha_final')
        print("hola")
        if fecha_inicio and fecha_final and fecha_inicio > fecha_final:
            print("error fecha")
            raise forms.ValidationError('La fecha de inicio no puede ser posterior a la fecha final.')

        return cleaned_data
    
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rol', 'correo', 'nombre_usuario', 'contrasena']
        widgets = {
            'rol': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('Administrador', 'Administrador'),
                ('Usuario', 'Usuario'),
            ]),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Usuario.objects.filter(correo=correo).exists():
            raise forms.ValidationError('Ya existe un usuario con este correo electrónico.')
        return correo

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get('contrasena')
        # Puedes agregar más validaciones aquí si es necesario
        return cleaned_data
    
class AsignarRecursoHumanoForm(forms.ModelForm):
    class Meta:
        model = RecursoHumano
        fields = ['usuario']

    def __init__(self, proyecto, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = Usuario.objects.filter(rol__nombre_rol__iexact='usuario')  # Filtra usuarios con rol 'usuario'
        self.instance.proyecto = proyecto
        self.proyecto = proyecto

    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')
        if RecursoHumano.objects.filter(proyecto=self.proyecto, usuario=usuario).exists():
            raise ValidationError('El usuario ya está asignado a este proyecto.')
        return usuario

class AgregarRecursoMaterialForm(forms.ModelForm):
    class Meta:
        model = RecursoMaterial
        fields = ['nombre_recurso', 'cantidad', 'descripcion']

    def __init__(self, proyecto, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.proyecto = proyecto

class AgregarDocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['descripcion', 'url_documento']

    def __init__(self, proyecto, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.proyecto = proyecto

class AgregarRiesgoForm(forms.ModelForm):
    class Meta:
        model = Riesgo
        fields = ['porcentaje_riesgo', 'descripcion_riesgo', 'plan_mitigacion_riesgo']

    def __init__(self, proyecto, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.proyecto = proyecto

class AgregarFaseForm(forms.ModelForm):
    class Meta:
        model = Fase
        fields = ['fase', 'concluido']

    def __init__(self, proyecto, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.proyecto = proyecto

        self.fields['fase'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre de la fase'
        })
        self.fields['concluido'].widget = forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })