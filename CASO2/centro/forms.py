import re
from django import forms
from django.utils import timezone
from django.utils.html import strip_tags
from .models import Paciente, Medico, Cita, Consulta


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ('dni', 'nombres', 'apellidos', 'fecha_nacimiento', 'tipo', 'codigo_uncp', 'alergias', 'email')
        widgets = {'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'})}

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if not re.fullmatch(r'\d{8}', dni):
            raise forms.ValidationError('El DNI debe tener 8 dígitos numéricos.')
        return dni

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data['fecha_nacimiento']
        if fecha > timezone.localdate():
            raise forms.ValidationError('La fecha de nacimiento no puede ser futura.')
        return fecha

    def clean_email(self):
        email = self.cleaned_data['email']
        if hasattr(self.instance, 'tipo') and self.instance.tipo == 'estudiante' and not email.endswith('@uncp.edu.pe'):
            raise forms.ValidationError('El email estudiantil debe terminar en @uncp.edu.pe.')
        return email


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ('medico', 'fecha', 'hora', 'motivo')
        widgets = {'fecha': forms.DateInput(attrs={'type': 'date'}), 'hora': forms.TimeInput(attrs={'type': 'time'})}

    def clean_motivo(self):
        motivo = strip_tags(self.cleaned_data['motivo']).strip()
        if len(motivo) < 20:
            raise forms.ValidationError('El motivo debe tener al menos 20 caracteres.')
        return motivo

    def clean(self):
        cleaned = super().clean()
        medico = cleaned.get('medico')
        fecha = cleaned.get('fecha')
        hora = cleaned.get('hora')
        motivo = cleaned.get('motivo')
        if fecha and hora:
            if hora < medico.horario_inicio or hora > medico.horario_fin:
                self.add_error('hora', 'La cita debe estar dentro del horario de atención.')
            if fecha.weekday() == 6:
                self.add_error('fecha', 'No hay atención los domingos.')
            if fecha.weekday() == 5 and hora > timezone.datetime.strptime('13:00', '%H:%M').time():
                self.add_error('hora', 'Los sábados atienden hasta las 13:00.')
        return cleaned


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ('diagnostico', 'tratamiento', 'medicamentos', 'proxima_cita', 'archivos_texto')
        widgets = {'proxima_cita': forms.DateInput(attrs={'type': 'date'})}
