import logging
from django.contrib import messages
from django.utils import timezone
from .models import Cita, MedicalAudit

logger = logging.getLogger('caso2.medico')


class MedicalAuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                ip = request.META.get('REMOTE_ADDR')
                accion = f'{request.method} {request.path}'
                MedicalAudit.objects.create(usuario=request.user, ip=ip, accion=accion)
                logger.info('usuario=%s ip=%s accion=%s', request.user, ip, accion)
            try:
                if hasattr(request.user, 'medico'):
                    pendientes = Cita.objects.filter(medico=request.user.medico, estado='pendiente', fecha__gte=timezone.localdate()).exists()
                    if pendientes:
                        messages.info(request, 'Tiene citas médicas pendientes.')
            except Exception:
                pass
        if '/historial/' in request.path and request.user.is_authenticated:
            logger.warning('Acceso a historial sensible: usuario=%s ip=%s', request.user, request.META.get('REMOTE_ADDR'))
        return self.get_response(request)
