from django.conf import settings
from django.db import models
from django.utils import timezone


class Laboratorio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    ESTADOS = (
        ('operativo', 'Operativo'),
        ('mantenimiento', 'En mantenimiento'),
        ('baja', 'Dado de baja'),
    )
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='operativo')
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.PROTECT)
    stock = models.PositiveIntegerField(default=1)
    ultimo_mantenimiento = models.DateField(default=timezone.localdate)

    @property
    def dias_sin_mantenimiento(self):
        return (timezone.localdate() - self.ultimo_mantenimiento).days

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Perfil(models.Model):
    ROLES = (('admin', 'Administrador'), ('docente', 'Docente'), ('asistente', 'Asistente'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)


class Prestamo(models.Model):
    ESTADOS = (('activo', 'Activo'), ('devuelto', 'Devuelto'), ('vencido', 'Vencido'))
    docente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='prestamos')
    equipo = models.ForeignKey(Equipo, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    observaciones = models.TextField(blank=True)

    @property
    def dias_retraso(self):
        if self.estado == 'devuelto':
            return 0
        return max(0, (timezone.localdate() - self.fecha_devolucion).days)

    def __str__(self):
        return f"{self.docente} - {self.equipo.codigo}"


class AuditLog(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    accion = models.CharField(max_length=255)
