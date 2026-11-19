from django.contrib import admin
from .models import Laboratorio, Equipo, Perfil, Prestamo, AuditLog


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'estado', 'laboratorio', 'dias_sin_mantenimiento')
    list_filter = ('laboratorio', 'estado')
    search_fields = ('codigo', 'nombre', 'categoria')
    actions = ['marcar_mantenimiento']

    @admin.action(description='Marcar como en mantenimiento')
    def marcar_mantenimiento(self, request, queryset):
        queryset.update(estado='mantenimiento')


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('docente', 'equipo', 'fecha_prestamo', 'fecha_devolucion', 'estado', 'dias_retraso')
    list_filter = ('estado', 'fecha_prestamo', 'docente')
    search_fields = ('equipo__codigo', 'equipo__nombre', 'docente__username', 'docente__first_name')
    actions = ['recordatorio']

    @admin.action(description='Enviar recordatorio de devolución')
    def recordatorio(self, request, queryset):
        self.message_user(request, f'Se enviaron {queryset.count()} recordatorios.')


admin.site.register(Laboratorio)
admin.site.register(Perfil)
admin.site.register(AuditLog)
