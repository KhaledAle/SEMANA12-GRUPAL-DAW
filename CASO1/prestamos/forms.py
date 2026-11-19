from django import forms
from django.utils.html import strip_tags
from django.utils import timezone
from .models import Equipo, Prestamo


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ('equipo', 'cantidad', 'fecha_prestamo', 'fecha_devolucion', 'observaciones')
        widgets = {
            'fecha_prestamo': forms.DateInput(attrs={'type': 'date'}),
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_observaciones(self):
        value = self.cleaned_data.get('observaciones', '')
        return strip_tags(value).strip()

    def clean(self):
        cleaned = super().clean()
        equipo = cleaned.get('equipo')
        cantidad = cleaned.get('cantidad')
        inicio = cleaned.get('fecha_prestamo')
        fin = cleaned.get('fecha_devolucion')
        if inicio and fin and fin <= inicio:
            self.add_error('fecha_devolucion', 'La devolución debe ser posterior al préstamo.')
        if equipo and equipo.estado != 'operativo':
            self.add_error('equipo', 'El equipo debe estar operativo.')
        if equipo and cantidad and cantidad > equipo.stock:
            self.add_error('cantidad', f'Solo hay {equipo.stock} unidades disponibles.')
        return cleaned


class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ('estado', 'observaciones')

