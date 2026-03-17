#!/usr/bin/env bash
set -euo pipefail

# Script de utilidad para destruir/limpiar recursos levantados por el proyecto.
# Uso:
#   ./scripts/teardown.sh dev     # Destruye recursos DEV (LocalStack + Terraform)
#   ./scripts/teardown.sh pro     # Destruye recursos PRO (AWS Terraform)
#   ./scripts/teardown.sh docker  # Para/borra contenedores Docker (MongoDB + LocalStack)
#   ./scripts/teardown.sh all     # Ejecuta docker + dev + pro (no recomendado si no estás seguro)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

function die() {
  echo "ERROR: $*" >&2
  exit 1
}

function ensure_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    die "Se requiere '$1' pero no está instalado o no está en el PATH."
  fi
}

function docker_cleanup() {
  ensure_command docker
  echo "Deteniendo y eliminando contenedores Docker usados por el proyecto..."

  docker compose -f "${ROOT_DIR}/docker-compose.dev.yml" down -v --remove-orphans || true

  # Con el task de VS Code se crea/usa un contenedor llamado "mongodb".
  docker rm -f mongodb 2>/dev/null || true
  docker rm -f backend-django-mongo 2>/dev/null || true
  docker rm -f backend-django-localstack 2>/dev/null || true

  echo "Contenedores Docker limpiados."
}

function terraform_destroy() {
  local env="$1"
  local tfdir="${ROOT_DIR}/infra/terraform"
  ensure_command terraform

  echo "Destruyendo recursos Terraform para el entorno: $env"
  pushd "$tfdir" >/dev/null

  # Asegurar que está inicializado
  terraform init -input=false >/dev/null

  if [[ "$env" == "dev" ]]; then
    terraform destroy -var-file=envs/dev.tfvars -auto-approve
  elif [[ "$env" == "pro" ]]; then
    terraform destroy -var-file=envs/pro.tfvars -auto-approve
  else
    die "Entorno desconocido: $env (usa 'dev' o 'pro')"
  fi

  popd >/dev/null
}

if [[ ${#@} -eq 0 ]]; then
  die "Especifica una acción: dev|pro|docker|all"
fi

case "$1" in
  dev)
    terraform_destroy dev
    ;;
  pro)
    terraform_destroy pro
    ;;
  docker)
    docker_cleanup
    ;;
  all)
    docker_cleanup
    terraform_destroy dev
    terraform_destroy pro
    ;;
  *)
    die "Opción desconocida: $1 (usa dev|pro|docker|all)"
    ;;
esac
