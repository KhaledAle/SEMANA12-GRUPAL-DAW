# Caso 2 - Centro Médico Universitario

Plataforma Django para pacientes, médicos, citas e historiales clínicos.

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
Incluye 8 médicos, 15 pacientes y 30 citas. Usuario administrador: `admin` / `admin123`.

## Diagrama de roles
`Paciente -> sus citas e historial propio`

`Médico -> agenda propia, consultas e historiales autorizados`

`Recepcionista -> agendar/cancelar citas y registrar pacientes`

`Administrador -> configuración, reportes y gestión total`
