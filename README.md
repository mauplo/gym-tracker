# Gym Tracker

Aplicación web para registrar rutinas de gimnasio, sesiones de entrenamiento y progreso (peso/repeticiones) por ejercicio a lo largo del tiempo. Cada usuario gestiona sus rutinas e historial de forma privada.

> Proyecto educativo para manejar desarrollo backend con Django, diseño de APIs REST, modelado de bases de datos relacionales y prácticas de seguridad.

## Características

- Registro de rutinas personalizadas combinando ejercicios de un catálogo compartido
- Catálogo de ejercicios con variantes por tipo de equipo (mancuerna, máquina, cable, etc.)
- Registro de sesiones de entrenamiento para medir consistencia
- Registro de series (peso, repeticiones) por ejercicio para medir progreso
- API REST documentada con autenticación por token
- Aislamiento de datos: cada usuario solo accede a su propia información

## Stack técnico

| Capa           | Tecnología                          |
|----------------|--------------------------------------|
| Backend        | Python 3.12, Django, Django REST Framework |
| Base de datos  | PostgreSQL 16                        |
| Auth           | Token Authentication (DRF)           |
| Documentación  | drf-spectacular (OpenAPI / Swagger)  |
| Testing        | pytest, pytest-django, factory-boy   |
| Contenedores   | Docker, Docker Compose               |

## Modelo de datos
User (Django built-in)
├──< Rutina
│ └──< RutinaEjercicio (M2M con Ejercicio: orden, series/reps objetivo)
├──< SesionEntrenamiento
│ └──< RegistroSerie (peso, reps, unidad, por ejercicio)
Ejercicio (catálogo global: nombre + tipo de equipo)

## Requisitos previos

- Python 3.12+
- Docker Desktop
- Git

## Instalación local

1. Clona el repositorio:
```bash
   git clone https://github.com/<tu-usuario>/gym-tracker.git
   cd gym-tracker
```

2. Crea y activa un entorno virtual:
```bash
   python -m venv venv
   source venv/bin/activate
```

3. Instala las dependencias:
```bash
   pip install -r requirements.txt
```

4. Copia el archivo de variables de entorno de ejemplo y ajústalo:
```bash
   cp .env.example .env
```

5. Levanta la base de datos con Docker:
```bash
   docker compose up -d
```

6. Aplica las migraciones:
```bash
   python manage.py migrate
```

7. Crea un superusuario:
```bash
   python manage.py createsuperuser
```

8. Corre el servidor de desarrollo:
```bash
   python manage.py runserver
```

La app estará disponible en `http://127.0.0.1:8000/`.

## Documentación de la API

Con el servidor corriendo:

- **Swagger UI (interactiva):** `http://127.0.0.1:8000/api/docs/`
- **Redoc (lectura):** `http://127.0.0.1:8000/api/redoc/`
- **Schema OpenAPI crudo:** `http://127.0.0.1:8000/api/schema/`
- **Panel de administración:** `http://127.0.0.1:8000/admin/`

### Autenticación

La API usa autenticación por token. Para obtener un token:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "tu_usuario", "password": "tu_password"}'
```

Luego incluye el token en cada request:

```bash
curl http://127.0.0.1:8000/api/rutinas/ \
  -H "Authorization: Token <tu-token>"
```

## Correr los tests

```bash
pytest -v
```

Para ver el reporte de cobertura:

```bash
pytest --cov=workouts
```

## Estructura del proyecto
gym-tracker/
├── config/ # Configuración del proyecto Django (settings, urls raíz)
├── workouts/ # App principal: modelos, API, tests
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│ ├── factories.py
│ └── tests/
├── docker-compose.yml # Definición del contenedor de PostgreSQL
├── requirements.txt
└── manage.py

## Roadmap

- [x] Modelado de datos y migraciones
- [x] API REST con permisos por usuario
- [x] Autenticación por token
- [x] Tests automatizados
- [x] Documentación OpenAPI
- [ ] Frontend con templates de Django
- [ ] Gráficas de progreso
- [ ] Deploy en producción (CI/CD con GitHub Actions)

## Licencia

MIT — ver [LICENSE](LICENSE).