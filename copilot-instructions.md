# Copilot Instructions (Project Conventions)

## Objetivo
Guiar a GitHub Copilot (y otros asistentes) para que proponga cambios consistentes con este proyecto Django orientado a microservicios.

## Convenciones clave

- **Entornos**: El proyecto distingue tres entornos mediante la variable `APP_ENV`:
  - `LOCAL`: ejecución local simple (por defecto) con MongoDB en `mongodb://localhost:27017`
  - `DEV`: entorno de desarrollo que usa **LocalStack** + Terraform (infraestructura emulada) y MongoDB local.
  - `PRO`: despliegue en AWS real (infraestructuras gestionadas por Terraform).

- **Configuración**: Variables de entorno esperadas:
  - `APP_ENV` (LOCAL|DEV|PRO)
  - `MONGO_URI` (cadena de conexión a MongoDB)
  - `MONGO_DB_NAME` (nombre de base de datos)

- **Infraestructura**: Existe un conjunto de configuraciones Terraform bajo `infra/terraform/` que se puede aplicar a cada entorno usando los `*.tfvars`.

## Arquitectura y Patrones (Django)
- **SOLID & Clean Architecture**: Mantén la lógica de negocio fuera de los `views.py`. Usa una capa de `services.py`.
- **Patrón Repositorio**: Usa `repositories.py` para aislar las llamadas a MongoDB (`pymongo`). No acoples la capa de base de datos directamente en las vistas.
- **Django Apps**: Estructura cada dominio de negocio (users, products) como una aplicación Django independiente (`python manage.py startapp`).

## Reglas de estilo / comportamiento

- Siempre que agregues nuevos servicios (p.ej. S3, DynamoDB, RDS) deberías habilitarlos bajo `infra/terraform/main.tf` y documentar cómo se emulan en `DEV` con LocalStack.
- No hardcodear credenciales ni endpoints; usa variables de entorno y/o `.tfvars`.

---

> Esta instrucción es un resumen de las decisiones de diseño del proyecto. Si deseas cambiar el comportamiento (p.ej. pasar MongoDB a Atlas, usar otra infra), actualiza este archivo y los archivos de configuración relacionados.
