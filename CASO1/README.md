# Caso 1 - Gestión de préstamos UNCP

Sistema Django para administrar laboratorios, equipos y préstamos.

## Instalación
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acceso administrador: `http://127.0.0.1:8000/admin/`

## Datos de prueba
La base local incluye 5 laboratorios, 10 equipos, 5 usuarios y 15 préstamos. Usuario administrador: `admin` / `admin123`.

## Roles
- Administrador: gestión completa.
- Docente: solicitud e historial propio.
- Asistente: devolución de préstamos.
- Invitado: catálogo público.
