# Terraform – Despliegue en AWS (Free Tier)

## Requisitos previos

1. **AWS CLI** configurado (`aws configure`)
2. **Terraform** instalado (`brew install terraform` o [terraform.io](https://terraform.io))
3. **Par de claves SSH** creado en AWS (EC2 → Key Pairs)
4. **MongoDB Atlas** (recomendado): cluster M0 gratuito en [atlas.mongodb.com](https://atlas.mongodb.com). Si la contraseña tiene caracteres especiales, URL-codifícala en la URI.

## Uso

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Editar terraform.tfvars con tus valores

terraform init
terraform plan
terraform apply
```

## Destruir recursos

```bash
terraform destroy
```
