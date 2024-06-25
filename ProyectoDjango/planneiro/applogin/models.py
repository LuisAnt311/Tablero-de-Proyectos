from django.db import models
from django.utils import timezone

# Create your models here.
#Usuarios
class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)
    descripcion_rol = models.TextField()

    def __str__(self):
        return self.nombre_rol

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    correo = models.EmailField(unique=True)
    nombre_usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_usuario

class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_proyecto = models.CharField(max_length=100)
    admin_proyecto_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='proyectos')
    estado = models.CharField(max_length=50)
    porcentaje = models.FloatField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    presupuesto = models.FloatField()
    costo_final = models.FloatField()
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_proyecto


class Impacto(models.Model):
    id = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='impactos')
    impacto = models.TextField()
    plan_de_impacto = models.TextField()

    def __str__(self):
        return f'Impacto del proyecto {self.proyecto.nombre_proyecto}'

class RecursoMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='recursos_materiales')
    cantidad = models.IntegerField()
    descripcion = models.TextField()
    nombre_recurso = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_recurso

class RecursoHumano(models.Model):
    id = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='recursos_humanos')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='recursos_humanos')

    def __str__(self):
        return f'{self.usuario.nombre_usuario} en proyecto {self.proyecto.nombre_proyecto}'

class Documento(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField(default='Descripción predeterminada')  # Define aquí tu valor por defecto
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='documentos')
    url_documento = models.URLField()

    def __str__(self):
        return f'Documento de proyecto {self.proyecto.nombre_proyecto}'

class Fase(models.Model):
    id = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='fases')
    fase = models.CharField(max_length=50)
    concluido = models.BooleanField()

    def __str__(self):
        return f'Fase {self.fase} de proyecto {self.proyecto.nombre_proyecto}'
    
class RelacionDocumento(models.Model):
    id = models.AutoField(primary_key=True)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='relaciones')
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, related_name='relaciones')
    
    def __str__(self):
        return f'Relación de Documento {self.documento.id} con Fase {self.fase.id}'

class Riesgo(models.Model):
    id = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='riesgos')
    porcentaje_riesgo = models.FloatField()
    descripcion_riesgo = models.TextField()
    plan_mitigacion_riesgo = models.TextField()

    def __str__(self):
        return f'Riesgo del proyecto {self.proyecto.nombre_proyecto}'

