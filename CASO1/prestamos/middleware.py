import logging
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver

logger = logging.getLogger('caso1.audit')


class AuditAndSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if request.user.is_authenticated:
            from .models import Prestamo, AuditLog
            vencidos = Prestamo.objects.filter(docente=request.user, estado='activo', fecha_devolucion__lt=timezone.localdate()).exists()
            if vencidos and not request.session.get('alerta_vencido'):
                messages.warning(request, 'Tiene préstamos vencidos. Debe devolverlos cuanto antes.')
                request.session['alerta_vencido'] = True
            if request.method in ('POST', 'DELETE'):
                accion = f'{request.method} {request.path}'
                AuditLog.objects.create(usuario=request.user, ip=ip, accion=accion)
                logger.info('usuario=%s ip=%s accion=%s', request.user, ip, accion)
        elif request.method == 'POST':
            logger.warning('Acceso no autorizado ip=%s path=%s', ip, request.path)
        return self.get_response(request)


@receiver(user_login_failed)
def login_failed(sender, credentials, request, **kwargs):
    ip = request.META.get('REMOTE_ADDR') if request else '?'
    logger.warning('Login fallido: ip=%s usuario=%s', ip, credentials.get('username'))
