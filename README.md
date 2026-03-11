# Libreta de Contactos con Django

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.8-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

Aplicación web desarrollada con Django que permite a los usuarios gestionar su propia libreta de contactos personal y privada. Cada usuario puede registrarse, iniciar sesión y administrar sus contactos de forma segura.

## Características

### Sistema de Autenticación
- **Registro de nuevos usuarios** con validación
- **Inicio y cierre de sesión** seguro
- **Protección de rutas** (solo usuarios autenticados)
- **Cambio de contraseña** integrado
- **Perfil de usuario** personalizable

### Gestión de Contactos
- **CRUD completo**: Crear, leer, actualizar y eliminar contactos
- **Campos completos**: 
  - Nombre completo
  - Teléfono (con validación)
  - Email (con validación)
  - Dirección
  - Fecha de nacimiento
  - Notas adicionales
- **Fotos de contacto** usando Pillow
- **Marcar favoritos** con actualización AJAX en tiempo real
- **Búsqueda avanzada** por nombre, teléfono o email
- **Filtro** por contactos favoritos
- **Paginación** (10 contactos por página)
- **Exportar a CSV** todos tus contactos

### Interfaz de Usuario
- **Diseño responsive** con Bootstrap 5
- **Iconos** de Font Awesome
- **Animaciones** suaves y transiciones
- **Notificaciones toast** para feedback instantáneo
- **Tooltips** informativos
- **Validación** de formularios en tiempo real
- **Modales** de confirmación para acciones críticas

### Seguridad
- **Aislamiento de datos**: Cada usuario solo ve sus propios contactos
- **Protección CSRF** en todos los formularios
- **Validación** de datos en servidor y cliente
- **Contraseñas hasheadas** con algoritmo seguro
- **Sesiones seguras** con timeout configurable

## Tecnologías

### Backend
- **Django 4.2** - Framework web principal
- **Python 3.8+** - Lenguaje de programación
- **SQLite** - Base de datos (por defecto)
- **Pillow** - Procesamiento de imágenes
- **Django REST Framework** - API REST

### Frontend
- **HTML5** - Estructura semántica
- **CSS3** - Estilos y animaciones
- **JavaScript** - Interactividad y AJAX
- **Bootstrap 5** - Framework CSS responsive
- **Font Awesome 6** - Iconografía

### Herramientas de Desarrollo
- **Git** - Control de versiones
- **pip** - Gestor de paquetes
- **virtualenv** - Aislamiento de entorno


## Instalación

### Requisitos Previos
- Python 3.8 o superior
- Git instalado
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```
git clone https://github.com/Raf150z/libreta-contactos.git
cd libreta-contactos
```
2. **Crear y activar entorno virtual**

Windows:
```
python -m venv venv
venv\Scripts\activate
```
Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```
3. **Instalar dependencias**
```
pip install -r requirements.txt
```
Realizar migraciones
```
python manage.py migrate
```
Crear superusuario (opcional, para acceder al panel admin)
```
python manage.py createsuperuser
```
Te pedirá: nombre de usuario, email y contraseña.

4. **Ejecutar servidor**
```
python manage.py runserver
```
5. **Acceder a la aplicación**
```
Página principal: http://localhost:8000
Panel de administración: http://localhost:8000/admin
```

## API
La aplicación incluye una API REST para integraciones:

Endpoint
```
http://localhost:8000/api/contactos/
```

## Autor

- **Rafael Velazquez**
- **GitHub: @Raf150z**
- **Proyecto: Libreta de Contactos**
