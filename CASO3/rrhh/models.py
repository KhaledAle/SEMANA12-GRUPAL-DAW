from django.conf import settings
from django.db import models
from django.utils import timezone


class Area(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self): return self.nombre


class Empleado(models.Model):
    CONTRATOS = (('planilla', 'Planilla'), ('locacion', 'Locación'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dni = models.CharField(max_length=8, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    fecha_ingreso = models.DateField()
    contrato = models.CharField(max_length=20, choices=CONTRATOS)
    email_corporativo = models.EmailField(unique=True)
    vacaciones_tomadas = models.PositiveIntegerField(default=0)

    @property
    def antiguedad(self):
        hoy = timezone.localdate()
        meses = (hoy.year - self.fecha_ingreso.year) * 12 + hoy.month - self.fecha_ingreso.month
        return f"{meses // 12} años y {meses % 12} meses"

    @property
    def vacaciones_disponibles(self):
        return max(0, 30 - self.vacaciones_tomadas)

    def __str__(self): return f"{self.nombres} {self.apellidos}"


class Asistencia(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.localdate)
    entrada = models.DateTimeField(null=True, blank=True)
    salida = models.DateTimeField(null=True, blank=True)
    horas_trabajadas = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    horas_extras = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def calcular(self):
        if self.entrada and self.salida:
            horas = (self.salida - self.entrada).total_seconds() / 3600
            self.horas_trabajadas = round(horas, 2)
            self.horas_extras = round(max(0, horas - 8), 2)

    def __str__(self): return f"{self.empleado} - {self.fecha}"


class Permiso(models.Model):
    TIPOS = (('personal', 'Personal'), ('medico', 'Médico'), ('duelo', 'Duelo'), ('maternidad', 'Maternidad/Paternidad'), ('otro', 'Otro'))
    ESTADOS = (('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado'))
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.TextField()
    adjunto_texto = models.CharField(max_length=255, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    @property
    def dias(self):
        return (self.fecha_fin - self.fecha_inicio).days + 1

    def __str__(self): return f"{self.empleado} - {self.tipo}"


class RRHHAudit(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True)
    accion = models.CharField(max_length=255)
