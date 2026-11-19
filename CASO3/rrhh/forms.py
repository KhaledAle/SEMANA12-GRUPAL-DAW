import re
from django import forms
from django.utils import timezone
from django.utils.html import strip_tags
from .models import Empleado, Permiso


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ('dni', 'nombres', 'apellidos', 'cargo', 'area', 'fecha_ingreso', 'contrato', 'email_corporativo')
        widgets = {'fecha_ingreso': forms.DateInput(attrs={'type': 'date'})}

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if not re.fullmatch(r'\d{8}', dni):
            raise forms.ValidationError('El DNI debe tener 8 dígitos.')
        return dni

    def clean_email_corporativo(self):
        email = self.cleaned_data['email_corporativo']
        if not email.endswith('@tecnoandes.pe'):
            raise forms.ValidationError('Debe usar un correo @tecnoandes.pe.')
        return email

    def clean_fecha_ingreso(self):
        fecha = self.cleaned_data['fecha_ingreso']
        if fecha > timezone.localdate():
            raise forms.ValidationError('La fecha de ingreso no puede ser futura.')
        return fecha

    def clean_cargo(self):
        cargo = strip_tags(self.cleaned_data['cargo']).strip()
        if not cargo:
            raise forms.ValidationError('El cargo no puede estar vacío.')
        return cargo


class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permiso
        fields = ('tipo', 'fecha_inicio', 'fecha_fin', 'motivo', 'adjunto_texto')
        widgets = {'fecha_inicio': forms.DateInput(attrs={'type': 'date'}), 'fecha_fin': forms.DateInput(attrs={'type': 'date'})}

    def clean_motivo(self):
        motivo = strip_tags(self.cleaned_data['motivo']).strip()
        if len(motivo) < 30:
            raise forms.ValidationError('El motivo debe tener al menos 30 caracteres.')
        return motivo

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get('fecha_inicio')
        fin = cleaned.get('fecha_fin')
        if inicio and fin:
            if fin < inicio:
                self.add_error('fecha_fin', 'La fecha final debe ser igual o posterior a la inicial.')
            if inicio > timezone.localdate():
                pass
        return cleaned
