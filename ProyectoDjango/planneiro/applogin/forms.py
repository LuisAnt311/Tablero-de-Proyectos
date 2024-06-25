from django import forms
from .models import Fase, Rol,Proyecto,Usuario

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
        fields = ['nombre_proyecto', 'admin_proyecto_usuario', 'estado', 'porcentaje', 'fecha_inicio', 'fecha_final', 'presupuesto', 'costo_final']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'type': 'date'}),
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
