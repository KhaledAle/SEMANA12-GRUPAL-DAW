from django.contrib import admin
from .models import Area, Empleado, Asistencia, Permiso, RRHHAudit


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'fecha', 'entrada', 'salida', 'horas_trabajadas', 'horas_extras')
    list_filter = ('fecha', 'empleado__area')
    search_fields = ('empleado__dni', 'empleado__nombres', 'empleado__apellidos')


@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'tipo', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'tipo', 'empleado__area')
    search_fields = ('empleado__nombres', 'empleado__apellidos')
    actions = ['aprobar']

    @admin.action(description='Aprobar permisos seleccionados')
    def aprobar(self, request, queryset):
        queryset.update(estado='aprobado')


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombres', 'apellidos', 'cargo', 'area', 'antiguedad', 'vacaciones_disponibles')
    search_fields = ('dni', 'nombres', 'apellidos')
    list_filter = ('area', 'contrato')


admin.site.register(Area)
admin.site.register(RRHHAudit)
