from django.conf import settings
from django.db import models
from django.utils import timezone


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self): return self.nombre


class Paciente(models.Model):
    TIPOS = (('estudiante', 'Estudiante'), ('docente', 'Docente'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dni = models.CharField(max_length=8, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    codigo_uncp = models.CharField(max_length=20)
    alergias = models.TextField(blank=True)
    email = models.EmailField()

    @property
    def edad(self):
        hoy = timezone.localdate()
        return hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    def __str__(self): return f"{self.nombres} {self.apellidos}"


class Medico(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cmp = models.CharField(max_length=20, unique=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT)
    consultorio = models.CharField(max_length=20)
    horario_inicio = models.TimeField(default='08:00')
    horario_fin = models.TimeField(default='18:00')
    def __str__(self): return f"Dr(a). {self.user.get_full_name() or self.user.username}"


class Cita(models.Model):
    ESTADOS = (('pendiente', 'Pendiente'), ('completada', 'Completada'), ('cancelada', 'Cancelada'))
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    def __str__(self): return f"{self.paciente} - {self.fecha} {self.hora}"


class Consulta(models.Model):
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE)
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    medicamentos = models.TextField(blank=True)
    proxima_cita = models.DateField(null=True, blank=True)
    archivos_texto = models.TextField(blank=True)


class MedicalAudit(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True)
    accion = models.CharField(max_length=255)
