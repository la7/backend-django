# -----------------------------------------------------------------------------
# Variables para despliegue en AWS (capa gratuita)
# -----------------------------------------------------------------------------

variable "aws_region" {
  description = "Región de AWS (us-east-1 recomendada para free tier)"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "Tipo de instancia EC2. t2.micro = free tier (750 h/mes, 12 meses)"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "Nombre del par de claves SSH existente en AWS para acceder a la instancia"
  type        = string
}

variable "repo_url" {
  description = "URL del repositorio Git (público) para clonar y construir la app"
  type        = string
}

variable "mongo_uri" {
  description = "URI de conexión a MongoDB (ej. MongoDB Atlas free tier)"
  type        = string
  sensitive   = true
}

variable "mongo_db" {
  description = "Nombre de la base de datos MongoDB"
  type        = string
  default     = "local"
}

variable "project_name" {
  description = "Prefijo para nombres de recursos"
  type        = string
  default     = "backend-django"
}
