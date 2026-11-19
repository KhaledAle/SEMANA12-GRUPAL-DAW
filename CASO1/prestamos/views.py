from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from .models import Equipo, Prestamo
from .forms import PrestamoForm, DevolucionForm


def catalogo(request):
    equipos = Equipo.objects.select_related('laboratorio').all()
    return render(request, 'prestamos/catalogo.html', {'equipos': equipos})


def iniciar_sesion(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('catalogo')
    return render(request, 'prestamos/login.html', {'form': form})


@login_required
def solicitar(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol not in ('admin', 'docente'):
        raise PermissionDenied
    form = PrestamoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        if Prestamo.objects.filter(docente=request.user, estado='activo').count() >= 3:
            form.add_error(None, 'No puede tener más de 3 préstamos activos.')
        else:
            prestamo = form.save(commit=False)
            prestamo.docente = request.user
            prestamo.save()
            prestamo.equipo.stock -= prestamo.cantidad
            prestamo.equipo.save(update_fields=['stock'])
            messages.success(request, 'Solicitud registrada correctamente.')
            return redirect('mis_prestamos')
    return render(request, 'prestamos/form.html', {'form': form, 'titulo': 'Solicitar equipo'})


@login_required
def mis_prestamos(request):
    prestamos = Prestamo.objects.select_related('equipo', 'docente').filter(docente=request.user)
    return render(request, 'prestamos/lista.html', {'prestamos': prestamos})


@login_required
def devolver(request, pk):
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'asistente':
        raise PermissionDenied
    prestamo = get_object_or_404(Prestamo.objects.select_related('equipo'), pk=pk)
    form = DevolucionForm(request.POST or None, instance=prestamo)
    if request.method == 'POST' and form.is_valid():
        devolucion = form.save(commit=False)
        devolucion.estado = 'devuelto'
        devolucion.save()
        prestamo.equipo.stock += prestamo.cantidad
        prestamo.equipo.save(update_fields=['stock'])
        messages.success(request, 'Devolución registrada.')
        return redirect('catalogo')
    return render(request, 'prestamos/form.html', {'form': form, 'titulo': 'Registrar devolución'})
