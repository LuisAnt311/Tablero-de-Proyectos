from django import forms
from .models import Fase, Rol

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