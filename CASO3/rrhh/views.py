from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import Empleado, Asistencia, Permiso
from .forms import PermisoForm


def inicio(request):
    asistencias = Asistencia.objects.select_related('empleado', 'empleado__area').all()[:30]
    return render(request, 'rrhh/inicio.html', {'asistencias': asistencias})


def iniciar_sesion(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('inicio')
    return render(request, 'rrhh/login.html', {'form': form})


@login_required
def marcar(request):
    if not hasattr(request.user, 'empleado'):
        raise PermissionDenied
    empleado = request.user.empleado
    ahora = timezone.now()
    registro = Asistencia.objects.filter(empleado=empleado, fecha=ahora.date()).first()
    if request.method == 'POST':
        if registro and registro.entrada and not registro.salida:
            registro.salida = ahora
            registro.calcular()
            registro.save()
            messages.success(request, 'Salida registrada.')
        elif registro and registro.entrada:
            messages.error(request, 'Ya tiene entrada y salida registradas hoy.')
        else:
            Asistencia.objects.create(empleado=empleado, fecha=ahora.date(), entrada=ahora)
            messages.success(request, 'Entrada registrada.')
        return redirect('inicio')
    return render(request, 'rrhh/form.html', {'titulo': 'Marcar asistencia'})


@login_required
def solicitar(request):
    if not hasattr(request.user, 'empleado'):
        raise PermissionDenied
    form = PermisoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        permiso = form.save(commit=False)
        permiso.empleado = request.user.empleado
        dias = permiso.dias
        if permiso.tipo == 'personal' and dias > permiso.empleado.vacaciones_disponibles:
            form.add_error('tipo', 'No tiene suficientes días disponibles.')
        else:
            superpuesto = Permiso.objects.filter(empleado=permiso.empleado, estado__in=('pendiente', 'aprobado'), fecha_inicio__lte=permiso.fecha_fin, fecha_fin__gte=permiso.fecha_inicio).exists()
            if superpuesto:
                form.add_error(None, 'Tiene un permiso superpuesto.')
            else:
                permiso.save()
                messages.success(request, 'Solicitud enviada para aprobación.')
                return redirect('inicio')
    return render(request, 'rrhh/form.html', {'form': form, 'titulo': 'Solicitar permiso'})
