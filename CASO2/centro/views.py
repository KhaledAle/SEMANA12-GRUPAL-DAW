from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cita, Consulta, Paciente
from .forms import CitaForm, ConsultaForm


def inicio(request):
    citas = Cita.objects.select_related('paciente', 'medico', 'medico__especialidad').all()[:20]
    return render(request, 'centro/inicio.html', {'citas': citas})


def iniciar_sesion(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('inicio')
    return render(request, 'centro/login.html', {'form': form})


@login_required
def agendar(request):
    if not (hasattr(request.user, 'paciente') or request.user.groups.filter(name='Recepcionistas').exists() or request.user.is_superuser):
        raise PermissionDenied
    form = CitaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cita = form.save(commit=False)
        cita.paciente = getattr(request.user, 'paciente', None)
        if cita.paciente is None:
            form.add_error(None, 'La recepcionista debe seleccionar un paciente.')
        else:
            duplicada = Cita.objects.filter(paciente=cita.paciente, fecha=cita.fecha, estado='pendiente').exists()
            ocupada = Cita.objects.filter(medico=cita.medico, fecha=cita.fecha, hora=cita.hora, estado='pendiente').exists()
            if duplicada:
                form.add_error('fecha', 'El paciente ya tiene una cita ese día.')
            elif ocupada:
                form.add_error('hora', 'El médico ya tiene una cita en ese horario.')
            else:
                cita.save()
                messages.success(request, 'Cita agendada correctamente.')
                return redirect('inicio')
    return render(request, 'centro/form.html', {'form': form, 'titulo': 'Agendar cita'})


@login_required
def historial(request, paciente_id):
    paciente = get_object_or_404(Paciente.objects.select_related('user'), pk=paciente_id)
    propio = hasattr(request.user, 'paciente') and request.user.paciente.pk == paciente.pk
    if not (propio or hasattr(request.user, 'medico') or request.user.is_superuser):
        raise PermissionDenied
    citas = Cita.objects.select_related('medico', 'medico__especialidad').filter(paciente=paciente)
    consultas = Consulta.objects.select_related('cita').filter(cita__paciente=paciente)
    return render(request, 'centro/historial.html', {'paciente': paciente, 'citas': citas, 'consultas': consultas})
