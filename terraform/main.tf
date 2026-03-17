# -----------------------------------------------------------------------------
# Terraform - Despliegue Backend Django en AWS (Free Tier)
# Servicios: EC2, Security Group, EBS
# -----------------------------------------------------------------------------

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project = var.project_name
      Managed = "terraform"
    }
  }
}

# Datos de la AMI más reciente de Amazon Linux 2
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Security Group: SSH (22), HTTP (80), Django (8000)
resource "aws_security_group" "app" {
  name        = "${var.project_name}-sg"
  description = "Permite SSH, HTTP y puerto Django"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Django"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-sg"
  }
}

# Instancia EC2 (t2.micro = free tier)
resource "aws_instance" "app" {
  ami                    = data.aws_ami.amazon_linux_2.id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.app.id]

  # 8 GB para permanecer en free tier (hasta 30 GB EBS)
  root_block_device {
    volume_size = 8
    volume_type = "gp2"
  }

  user_data = <<-EOF
    #!/bin/bash
    set -e
    yum update -y
    yum install -y docker git
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ec2-user

    # Clonar, construir y ejecutar
    cd /home/ec2-user
    git clone ${var.repo_url} app || true
    cd app
    docker build -t backend-django .
    docker run -d --name api -p 8000:8000 \
      -e MONGO_URI="${var.mongo_uri}" \
      -e MONGO_DB="${var.mongo_db}" \
      --restart unless-stopped \
      backend-django
  EOF

  tags = {
    Name = "${var.project_name}-ec2"
  }
}
