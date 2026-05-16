# Medical Consults API
Una pequeña aplicación web construida con Flask para gestionar usuarios (roles: Admin, Médico, Paciente) y citas médicas.

Este repositorio contiene un ejemplo de aplicación con: registro y login de usuarios, creación/edición/eliminación de citas, cambio de contraseña, y un script para crear usuarios de demostración.

## Contenido

- `run.py` - punto de entrada para ejecutar la aplicación.
- `config.py` - configuración básica (clave secreta, URI de la base de datos).
- `create_demo_users.py` - script para crear roles y usuarios de ejemplo.
- `requirements.txt` - dependencias de Python.
- `app/` - paquete principal de la aplicación:
	- `__init__.py` - fábrica de la aplicación, inicializa extensiones y registra blueprints.
	- `models.py` - modelos de la base de datos (Role, User, Appointment).
	- `forms.py` - formularios con Flask-WTF.
	- `auth_routes.py` - rutas para autenticación (login, register, logout).
	- `routes.py` - rutas principales (dashboard, gestionar citas, usuarios, cambiar contraseña).
	- `templates/` - plantillas HTML para las vistas.

## Requisitos

- Python 3.8+ (se recomienda 3.10 o 3.11).
- Las dependencias están listadas en `requirements.txt`.

Instalar dependencias (por ejemplo en macOS con zsh):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Si usas un entorno global, ajusta los comandos según tus preferencias.

## Variables de entorno y configuración

El archivo `config.py` lee opcionalmente las siguientes variables de entorno:

- `SECRET_KEY` - clave secreta para Flask (por defecto: `clave-secreta-123`).
- `DATABASE_URL` - URI de la base de datos (por defecto usa SQLite `sqlite:///database.db`).

Puedes exportarlas en tu entorno antes de ejecutar la app:

```bash
export SECRET_KEY="mi_clave_secreta"
export DATABASE_URL="sqlite:///database.db"
```

## Crear la base de datos y usuarios de demostración

1. Crea las tablas y usuarios de demo ejecutando el script proporcionado:

```bash
source venv/bin/activate
python create_demo_users.py
```

Esto hará lo siguiente:
- Creará las tablas en la base de datos configurada.
- Añadirá los roles `Admin`, `Medico` y `Paciente` (si no existen).
- Creará tres usuarios de ejemplo:
	- admin@example.com / admin123 (rol Admin)
	- medico@example.com / medico123 (rol Medico)
	- paciente@example.com / paciente123 (rol Paciente)

Nota: el script imprime mensajes indicando si un rol o usuario ya existía.

## Ejecutar la aplicación

Ejecutar localmente con Flask (modo de desarrollo):

```bash
source venv/bin/activate
python run.py
```

La aplicación por defecto se ejecutará en `http://127.0.0.1:5000/` con `debug=True` (ver `run.py`).

## Rutas principales y comportamiento

Autenticación (`app/auth_routes.py`):
- `GET /login` - muestra formulario de login.
- `POST /login` - autentica por `email` y `password`.
- `GET /register` - muestra formulario de registro.
- `POST /register` - crea un usuario (requiere seleccionar rol `Paciente` o `Medico`).
- `GET /logout` - cierra sesión.

Vistas principales (`app/routes.py`):
- `GET /` - página de inicio.
- `GET /dashboard` - panel de usuario. Contenido dependiendo del rol:
	- Paciente: muestra sus citas.
	- Médico: muestra citas donde es médico.
	- Admin: ve todas las citas.
- `GET, POST /citas/crear` - permite a pacientes crear una cita. El formulario espera el campo `fecha` en formato `YYYY-MM-DD HH:MM` y `motivo`.
- `GET, POST /citas/<id>/editar` - paciente (dueño) o admin puede editar la cita.
- `POST /citas/<id>/eliminar` - paciente (dueño) o admin puede eliminar la cita.
- `GET, POST /cambiar-password` - formulario para cambiar la contraseña (valida contraseña actual).
- `GET /usuarios` - solo admin: lista usuarios.
- `POST /usuarios/<id>/eliminar` - solo admin: elimina usuario (no puede eliminarse a sí mismo).

Nota: las rutas usan Flask-Login y requieren autenticación donde corresponde.

## Modelos principales

Definidos en `app/models.py`:

- Role:
	- id, name
	- relación con `User` (un role tiene muchos usuarios)
- User (hereda de UserMixin):
	- id, username, email, password_hash, role_id
	- métodos: `set_password`, `check_password`
	- relaciones: `citas_paciente`, `citas_medico`
- Appointment:
	- id, fecha (DateTime), motivo, status (por defecto `pendiente`), paciente_id, medico_id

Las contraseñas se almacenan en `password_hash` usando Werkzeug (hash seguro).

## Formularios

Definidos en `app/forms.py` con Flask-WTF:
- `LoginForm`: email, password
- `RegisterForm`: username, email, password, confirm_password, role (Paciente/Medico)
- `ChangePasswordForm`: old_password, new_password, confirm_password
- `AppointmentForm`: fecha (texto, formato `YYYY-MM-DD HH:MM`), motivo

## Dependencias

Listado en `requirements.txt` (principales):
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- email-validator
- PyMySQL (opcional, si usas MySQL)

Instala con `pip install -r requirements.txt`.

## Buenas prácticas y notas

- En producción, fija `SECRET_KEY` y `DATABASE_URL` en variables de entorno seguras.
- Considera usar un servidor WSGI (gunicorn/uwsgi) y desactivar `debug`.
- Validación de fechas: actualmente la app espera que el usuario ingrese la fecha como texto. Se recomienda mejorar la UX con un selector de fecha/hora en el frontend o validar/normalizar entradas en el servidor.
- Asignación de `medico_id` al crear citas está temporalmente fijada a `1` en `routes.py` (comentado "esto lo mejoraremos despues"). Debes cambiar la lógica para permitir seleccionar médico o asignar automáticamente uno disponible.
- El modelo y las vistas son simples; si planeas exponer una API REST, es recomendable añadir endpoints JSON separados y protección CSRF/token según el caso.

## Tests y ejemplos de peticiones

En la carpeta `pruebas/` tienes ejemplos en formato REST (archivos `.rest`) para probar operaciones CRUD:
- `create.rest`, `read.rest`, `read-a-row.rest`, `update.rest`, `delete.rest`.

Puedes usar herramientas como REST Client (extensión de VS Code), curl o Postman para probar las rutas.

Ejemplo rápido con curl (login y obtener dashboard no autenticado con sesión no funcionará sin manejar cookies; se recomienda usar el navegador o herramientas que mantengan sesión):

```bash
# Crear la BD y usuarios demo
python create_demo_users.py

# Ejecutar la app
python run.py
```

Luego abre `http://127.0.0.1:5000/` en el navegador e inicia sesión con los usuarios de ejemplo.

