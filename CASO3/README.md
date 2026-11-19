# Caso 3 - Control de asistencia TecnoAndes

Sistema Django para empleados, áreas, asistencia y permisos.

## Instalación
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Datos de prueba
Incluye 5 áreas, 10 empleados, 50 asistencias y 10 permisos. Usuario administrador: `admin` / `admin123`.
