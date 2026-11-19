# Practica Grupal Semana 12 - Desarrollo de Aplicaciones Web

Repositorio general con los tres casos requeridos para la Unidad II: Gestion Web Fullstack con Django.

Repositorio: https://github.com/KhaledAle/SEMANA12-GRUPAL-DAW

## Casos incluidos

| Caso | Carpeta | Sistema |
|---|---|---|
| Caso 1 | [`CASO1`](./CASO1) | Gestion de prestamos de equipos de laboratorio |
| Caso 2 | [`CASO2`](./CASO2) | Gestion de consultas medicas |
| Caso 3 | [`CASO3`](./CASO3) | Control de asistencia y permisos de empleados |

Cada carpeta es un proyecto Django independiente y contiene su propio `README.md`, base de datos de prueba, migraciones, modelos, formularios, Django Admin, middleware y plantillas.

## Requisitos generales

- Python 3.11 o superior
- Pip
- Git

Los proyectos usan Django 6.1.

## Instalacion general

Clone el repositorio desde PowerShell:

```powershell
git clone https://github.com/KhaledAle/SEMANA12-GRUPAL-DAW.git
cd SEMANA12-GRUPAL-DAW
```

Cada proyecto debe ejecutarse desde su propia carpeta. Cree un entorno virtual dentro de esa carpeta:

```powershell
cd CASO1
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Repita el proceso cambiando `CASO1` por `CASO2` o `CASO3`.

URLs locales:

- Caso 1: http://127.0.0.1:8000/
- Caso 2: http://127.0.0.1:8000/
- Caso 3: http://127.0.0.1:8000/
- Administracion de Django: http://127.0.0.1:8000/admin/

Importante: ejecute cada proyecto en una terminal distinta y detenga el servidor anterior antes de iniciar el siguiente.

## Instalacion por caso

### Caso 1 - Gestion de prestamos

```powershell
cd CASO1
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Incluye gestion de equipos, prestamos, devoluciones, validaciones, sesiones, roles, auditoria y Django Admin personalizado.

### Caso 2 - Gestion de consultas medicas

```powershell
cd CASO2
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Incluye pacientes, medicos, citas, consultas, historiales, permisos por rol, auditoria medica y agenda administrable.

### Caso 3 - Asistencia y permisos

```powershell
cd CASO3
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Incluye empleados, areas, registro de asistencia, horas extras, solicitudes de permisos, aprobacion jerarquica y reportes.

## Datos de prueba

Los proyectos ya incluyen datos demostrativos cargados en sus bases SQLite locales:

- Caso 1: 5 laboratorios, 10 equipos, 5 usuarios y 15 prestamos.
- Caso 2: 8 medicos, 15 pacientes y 30 citas.
- Caso 3: 5 areas, 10 empleados, 50 registros de asistencia y 10 permisos.

Credenciales administrativas de demostracion:

- Usuario: `admin`
- Contraseña: `admin123`

Cada caso permite crear o cargar mas datos desde Django Admin.

## Funcionalidades generales

- Formularios con `ModelForm`, formularios clasicos, validaciones `clean()` y `clean_<campo>()`.
- Sanitizacion de textos observables.
- Django Admin con filtros, busquedas, campos calculados y acciones masivas.
- Middleware propio de auditoria y controles especializados.
- Login/logout y autorizacion basada en usuarios, roles y grupos.
- Sesiones configuradas con timeout segun el caso.
- Cookies de sesion HttpOnly y proteccion CSRF.
- Consultas relacionadas mediante `select_related()`.
- Repositorios separados por cada caso y archivos de instalacion independientes.

## Seguridad

Las credenciales de demostracion son solamente para laboratorio. Antes de publicar el proyecto en produccion:

1. Cambie `SECRET_KEY`.
2. Configure `DEBUG = False`.
3. Configure `ALLOWED_HOSTS`.
4. Habilite `SESSION_COOKIE_SECURE = True`.
5. Habilite `CSRF_COOKIE_SECURE = True`.
6. Cambie todas las contraseñas de prueba.

## Administracion

Ingrese a `/admin/` con las credenciales administrativas de demostracion para probar:

- Registros y filtros.
- Acciones masivas.
- Campos calculados.
- Busesquedas.
- Permisos de usuario y grupos.

## Ejecucion de comprobaciones

Desde cada carpeta:

```powershell
python manage.py check
python manage.py test
```
