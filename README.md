## Backend Django – Proyecto de ejemplo empresarial

API REST construida con **Django y Django REST Framework (DRF)** que muestra patrones empresariales basados en SOLID:
- **Apps separadas por dominio** (`products`, `users`, `auth`).
- **Autenticación** con **OAuth2**:
  - Autenticación básica con token sencillo.
  - Autenticación con **JWT** y contraseñas cifradas con **bcrypt/passlib**.
- **Persistencia** en **MongoDB** para usuarios, usando **pymongo**.
- Servido de **estáticos** (imágenes) desde la carpeta `static`.

---

### Tecnologías y dependencias principales

- **Lenguaje**: Python 3.x
- **Framework**: Django & Django REST Framework (DRF)
- **Librerías clave** (de `requirements.txt`):
  - `django`: Framework web principal.
  - `djangorestframework`: Construcción de la API REST.
  - `drf-spectacular`: Generación automática de **Swagger/OpenAPI 3**.
  - `gunicorn`: Servidor de aplicaciones WSGI para producción.
  - `djangorestframework-simplejwt`: Manejo de autenticación JWT.
  - `pymongo`: cliente para conectarse a **MongoDB**.

---

### Estructura general de la solución

Basada en los principios **SOLID** y diseño de microservicios:

- `core/`: Configuración principal del proyecto (`settings.py`, `urls.py`).
- `apps/products/` y `apps/users/`: Módulos de dominio. Cada app contiene:
  - `views.py` (Controladores HTTP).
  - `services.py` (Lógica de negocio).
  - `repositories.py` (Abstracción de acceso a MongoDB).
  - `serializers.py` (Validación de datos, equivalente a Pydantic).

---

### Manejo de errores y respuestas estándar

- **Excepciones de DRF (`APIException`)**:
  - `NotFound`, `ValidationError`, `PermissionDenied`.
- **Respuestas personalizadas en routers**:
  - Manejadas en views o a través de un Custom Exception Handler global.
- **Validación con Serializers**:
  - Garantizan que la estructura de los datos de entrada/salida sea estricta.

---

### Ejecución en local

Desde la raíz del proyecto, te recomendamos crear un **entorno virtual** para aislar las dependencias:

```bash
# 1. Crear el entorno virtual
python3 -m venv venv

# 2. Activar el entorno virtual
# En Mac/Linux:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# 3. Instalar las dependencias
pip install -r requirements.txt

# 4. Levantar el servidor de desarrollo
python manage.py runserver 0.0.0.0:8000
```

- El servidor se levantará en `http://127.0.0.1:8000` (o `http://0.0.0.0:8000` cuando se ejecuta dentro de un contenedor).
- `--reload` recarga automáticamente cuando se modifican los archivos, ideal para desarrollo.
- Si no ejecutas este comando, no habrá un servicio escuchando y `curl http://localhost:8000` dará "connection refused".

**Alternativa con Docker (local):**

```bash
docker build -t backend-django .
docker run -p 8000:8000 -e MONGO_URI=mongodb://host.docker.internal:27017 backend-django
```

(Requiere MongoDB en local o usar `MONGO_URI` de MongoDB Atlas.)

---

### URLs útiles para pruebas

Dependiendo de cómo ejecutes el proyecto, estos son los endpoints más comunes:

- **Local (Django runserver)**
  - Base API: `http://localhost:8000/api/`
  - Swagger UI: `http://localhost:8000/api/docs/`
  - ReDoc: `http://localhost:8000/api/redoc/`
  - OpenAPI Schema: `http://localhost:8000/api/schema/`

- **Docker (contenedor del proyecto)**
  - Base API: `http://localhost:8000/api/`
  - Swagger UI: `http://localhost:8000/api/docs/`

- **Terraform / AWS (PRO)**
  - Base API: `http://<EC2_PUBLIC_IP>:8000/api/`
  - Swagger UI: `http://<EC2_PUBLIC_IP>:8000/api/docs/`

> Nota: en el entorno DEV (LocalStack) el endpoint se monta en `http://localhost:4566`, pero la API en el contenedor sigue expuesta en `:8000`.

---

### MongoDB en local: Docker + launch (VS Code / Cursor)

Para evitar instalar MongoDB en la máquina, el proyecto usa **MongoDB en Docker** y lo integra con el **launch** del IDE.

#### Archivos involucrados

| Archivo | Uso |
|--------|-----|
| `.vscode/tasks.json` | Tareas: **Docker: MongoDB** (arrancar contenedor) y **Docker: stop MongoDB** (parar contenedor). |
| `.vscode/launch.json` | Configuración **django (uvicorn)** con `preLaunchTask: "Docker: MongoDB"`. |

#### Comportamiento

1. **Al dar Run/Debug (F5)** con la configuración **"django (uvicorn)"**:
   - Se ejecuta primero la tarea **Docker: MongoDB**: si existe el contenedor `mongodb` se hace `docker start`; si no, se crea con `docker run -d -p 27017:27017 --name mongodb mongo:latest`.
   - Luego se inicia uvicorn; la API usa `localhost:27017` (por defecto en `app/db/client.py`).

2. **Al dar Stop** en el IDE:
   - Solo se detiene el proceso **django/uvicorn**. El contenedor **MongoDB sigue en ejecución** (Docker lo gestiona por separado).

3. **Para parar MongoDB** cuando termines:
   - Desde terminal: `docker stop mongodb`
   - O en el IDE: **Terminal → Run Task… → "Docker: stop MongoDB"**.

#### Requisito

- **Docker** instalado y en ejecución (Docker Desktop o daemon de Docker).

#### Comandos manuales (sin launch)

```bash
# Arrancar MongoDB (si no usas el launch)
docker start mongodb 2>/dev/null || docker run -d -p 27017:27017 --name mongodb mongo:latest

# Ver si está corriendo
docker ps | grep mongodb

# Parar MongoDB
docker stop mongodb
```

---

### Cómo detener el servidor (procesos Uvicorn)

Si has lanzado Uvicorn desde la terminal y quieres cerrar **todos los procesos de uvicorn**:

```bash
pkill -f uvicorn
```

### Configuración del IDE (PyCharm / VS Code)

Para ejecutar y depurar el proyecto directamente desde tu IDE, asegúrate de configurar un "Run/Debug Configuration" que ejecute el comando `manage.py runserver`.



### Documentación interactiva (Swagger / ReDoc)

Django (vía `drf-spectacular`) genera automáticamente la documentación OpenAPI a partir de:
- Vistas y ViewSets de Django REST Framework.
- Serializers (que validan y estructuran la entrada/salida).
- Metadatos de la aplicación (`title`, `description`, `version`).

Con el servidor levantado (`python manage.py runserver`), puedes acceder a:

- **Swagger UI (documentación interactiva)**  
  - URL: `http://127.0.0.1:8000/api/docs/`
  - Permite:
    - Ver todos los endpoints agrupados por `tags`.
    - Explorar métodos, parámetros, modelos de entrada/salida.
    - Probar endpoints con **“Try it out”**, incluyendo autenticación vía token.

- **ReDoc (documentación alternativa)**  
  - URL: `http://127.0.0.1:8000/api/redoc/`
  - Vista más orientada a lectura de la especificación OpenAPI completa.

---

### Despliegue en AWS con Terraform (capa gratuita)

El proyecto incluye configuración de **Terraform** para desplegar la API en **AWS** usando recursos de la **capa gratuita**. La aplicación sigue funcionando igual en local; el despliegue en AWS es opcional.

#### Servicios de AWS utilizados

| Servicio | Uso | Capa gratuita |
|----------|-----|----------------|
| **EC2** | Instancia para ejecutar la API (Docker) | 750 h/mes de `t2.micro` durante 12 meses |
| **EBS** | Volumen de disco para la instancia | 30 GB de almacenamiento gp2 |
| **Security Group** | Reglas de firewall (SSH, HTTP, django) | Sin coste adicional |
| **VPC** | Red por defecto | Incluida |

**MongoDB**: No se usa DocumentDB (de pago). Se recomienda **MongoDB Atlas** (cluster M0 gratuito) y configurar `MONGO_URI` en Terraform.

#### Requisitos previos

- Cuenta AWS con capa gratuita activa
- [AWS CLI](https://aws.amazon.com/cli/) configurado (`aws configure`)
- [Terraform](https://terraform.io) instalado
- Par de claves SSH creado en AWS (EC2 → Key Pairs)
- Repositorio Git público (o URL del repo que quieras desplegar)
- Cluster MongoDB Atlas (opcional, gratuito) para el router `userdb`

#### Pasos para desplegar

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Editar terraform.tfvars: key_name, repo_url, mongo_uri

terraform init
terraform plan
terraform apply
```

Tras `apply`, Terraform mostrará la IP pública y las URLs de la API y la documentación.

#### Estructura de archivos Terraform

- `terraform/main.tf`: proveedor AWS, AMI, Security Group, instancia EC2 y user_data
- `terraform/variables.tf`: variables (región, tipo de instancia, clave SSH, repo, MongoDB)
- `terraform/outputs.tf`: IP, URLs de la API, Swagger y ReDoc
- `terraform/terraform.tfvars.example`: plantilla de variables (copiar a `terraform.tfvars`)

#### Comportamiento en local vs AWS

| Entorno | MongoDB | Ejecución |
|---------|---------|-----------|
| **Local** | `mongodb://localhost:27017` (por defecto) | `python manage.py runserver` |
| **AWS** | `MONGO_URI` y `MONGO_DB` vía variables de entorno | Gunicorn dentro de un contenedor Docker en EC2. |

La configuración de la base de datos (`core/settings.py`) usa las variables de entorno `MONGO_URI` y `MONGO_DB_NAME`; si no están definidas, usa valores por defecto para desarrollo local.

#### Destruir recursos de Terraform (DEV / PRO)

**DEV (LocalStack + Terraform):**

```bash
cd infra/terraform
terraform init
terraform destroy -var-file=envs/dev.tfvars -auto-approve
```

**PRO (AWS):**

```bash
cd infra/terraform
terraform init
terraform destroy -var-file=envs/pro.tfvars -auto-approve
```

> 💡 Tip: si utilizas el script de utilidad, puedes correr `./scripts/teardown.sh dev` o `./scripts/teardown.sh pro`.

---

### Detener y eliminar contenedores Docker (MongoDB / LocalStack)

El proyecto usa Docker para MongoDB (y opcionalmente LocalStack, en DEV).

Opcion 1
```bash
cd terraform
terraform destroy
```

Opcion 2
```bash
# Detiene y borra contenedores + volúmenes del entorno DEV:
docker compose -f docker-compose.dev.yml down -v

# También elimina contenedores creados por las tareas de VS Code (opcional):
docker rm -f mongodb backend-django-mongo backend-django-localstack 2>/dev/null || true
```

> 💡 Tip: el script de utilidad (`./scripts/teardown.sh docker`) hace lo anterior de forma segura.

---

### Notas finales

- El proyecto está pensado como base de proyecto profesional de:
  - Organización por routers y capas (routers, db, modelos, esquemas).
  - Distintos mecanismos de autenticación (simple y con JWT).
  - Integración con base de datos MongoDB.
- A partir de esta estructura, es sencillo:
  - Añadir nuevos dominios (nuevos routers).
  - Ampliar modelos y reglas de negocio.
  - Sustituir o extender la capa de persistencia según necesidades reales.

---

## Entornos y despliegue (LOCAL / DEV / PRO)

Este proyecto soporta tres entornos principales:

- **LOCAL**: desarrollo rápido en tu máquina (por defecto). Usa MongoDB local (`mongodb://localhost:27017`).
- **DEV**: entorno de desarrollo basado en **LocalStack + Terraform**, que emula infra de AWS en tu máquina.
- **PRO**: despliegue real en **AWS** (infra gestionada por Terraform).

### Configuración de entorno

Los ajustes se controlan con variables de entorno:

- `APP_ENV` (valores: `LOCAL`, `DEV`, `PRO`) — determina el modo de ejecución.
- `MONGO_URI` — cadena de conexión a MongoDB.
- `MONGO_DB_NAME` — nombre de la base de datos a usar.

**Ejemplo (local):**

```bash
export APP_ENV=LOCAL
export MONGO_URI="mongodb://localhost:27017"
export MONGO_DB_NAME="local"
python manage.py runserver
```

### Levantar el entorno DEV (LocalStack + Terraform)

**Nota sobre la infraestructura:** Terraform es una herramienta de Infraestructura como Código (IaC). Su única función es crear los recursos simulados (S3, DynamoDB, etc.), no ejecuta tu código Python. Toda la lógica de negocio (`users`, `products`) vive en tus apps de Django y se corre por separado.

1) Levanta los servicios de desarrollo (LocalStack + MongoDB):

```bash
docker compose -f docker-compose.dev.yml up -d
```

2) Inicializa/aplica Terraform en el entorno `dev`:

```bash
cd infra/terraform
terraform init
terraform apply -var-file=envs/dev.tfvars -auto-approve
```

LocalStack expondrá endpoints AWS en `http://localhost:4566`.

> Nota: el ejemplo de Terraform crea un bucket S3 y una tabla DynamoDB en el entorno `DEV`.

3) Ejecuta tu API Django apuntando a DEV:

```bash
export APP_ENV=DEV
export MONGO_URI="mongodb://localhost:27017"
export MONGO_DB_NAME="local"
python manage.py runserver 0.0.0.0:8000
```

### Eliminar el entorno DEV

Para destruir la infraestructura y detener los contenedores de forma segura, utiliza el script de utilidad incluido (ejecútalo desde la raíz del proyecto):

- **Destruir solo la infraestructura emulada en LocalStack:**
  ```bash
  ./scripts/teardown.sh dev
  ```
- **Apagar y limpiar contenedores Docker (LocalStack y MongoDB):**
  ```bash
  ./scripts/teardown.sh docker
  ```
- **Destruir infraestructura y contenedores de un solo golpe:**
  ```bash
  ./scripts/teardown.sh all
  ```

### Despliegue a AWS (PRO)

1) Configura tus credenciales AWS (por ejemplo, `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`).
2) Ejecuta Terraform con las variables de `PRO`:

```bash
cd infra/terraform
terraform init
terraform apply -var-file=envs/pro.tfvars -auto-approve
```

> Para entornos de producción reales, ajusta `infra/terraform/main.tf` para definir todos los recursos que necesites (ECS/ECR, DocumentDB, VPC, etc.).

## Monitor Estatus
```bash
docker ps | grep localstack
docker ps | grep mongo
ps aux | grep [u]vicorn
```