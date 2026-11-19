from django.contrib import admin
from .models import Especialidad, Paciente, Medico, Cita, Consulta, MedicalAudit


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'fecha', 'hora', 'estado')
    list_filter = ('fecha', 'estado', 'medico')
    search_fields = ('paciente__dni', 'paciente__nombres', 'paciente__apellidos')
    actions = ['completar']

    @admin.action(description='Marcar citas como completadas')
    def completar(self, request, queryset):
        queryset.update(estado='completada')


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombres', 'apellidos', 'edad', 'tipo')
    search_fields = ('dni', 'nombres', 'apellidos')
    list_filter = ('tipo',)


admin.site.register(Especialidad)
admin.site.register(Medico)
admin.site.register(Consulta)
admin.site.register(MedicalAudit)
