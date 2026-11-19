import logging
from django.contrib import messages
from django.utils import timezone
from .models import Asistencia, RRHHAudit

logger = logging.getLogger('caso3.rrhh')


class AttendanceAuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not request.user.is_active:
                from django.contrib.auth import logout
                logout(request)
            if request.method == 'POST':
                ip = request.META.get('REMOTE_ADDR')
                accion = f'{request.method} {request.path}'
                RRHHAudit.objects.create(usuario=request.user, ip=ip, accion=accion)
                logger.info('usuario=%s ip=%s accion=%s', request.user, ip, accion)
            if hasattr(request.user, 'empleado'):
                hoy = timezone.localdate()
                marcada = Asistencia.objects.filter(empleado=request.user.empleado, fecha=hoy, entrada__isnull=False).exists()
                if hoy.weekday() < 5 and not marcada:
                    messages.info(request, 'Recuerde marcar su entrada del día.')
        return self.get_response(request)
