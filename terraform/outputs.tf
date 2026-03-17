# -----------------------------------------------------------------------------
# Outputs tras aplicar Terraform
# -----------------------------------------------------------------------------

output "instance_id" {
  description = "ID de la instancia EC2"
  value       = aws_instance.app.id
}

output "public_ip" {
  description = "IP pública de la instancia"
  value       = aws_instance.app.public_ip
}

output "api_url" {
  description = "URL base de la API (django en puerto 8000)"
  value       = "http://${aws_instance.app.public_ip}:8000"
}

output "docs_url" {
  description = "URL de documentación Swagger"
  value       = "http://${aws_instance.app.public_ip}:8000/docs"
}

output "redoc_url" {
  description = "URL de documentación ReDoc"
  value       = "http://${aws_instance.app.public_ip}:8000/redoc"
}

output "ssh_command" {
  description = "Comando para conectarse por SSH"
  value       = "ssh -i <tu-clave.pem> ec2-user@${aws_instance.app.public_ip}"
}
