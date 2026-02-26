provider "aws" {
  region = var.aws_region
}

# Use default VPC for simplicity in this project
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Security Group for EC2
resource "aws_security_group" "airlines_sg" {
  name        = "airlines-sg"
  description = "Allow HTTP and SSH inbound traffic"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
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
    Name = "AirlinesAppSG"
  }
}

# Find the latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# IAM Role for EC2 (Optional, useful if interacting with other AWS services like S3 or ECR)
resource "aws_iam_role" "ec2_role" {
  name = "airlines_ec2_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "airlines_ec2_profile"
  role = aws_iam_role.ec2_role.name
}

# EC2 Instance to host the Docker containers
resource "aws_instance" "app_server" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = var.instance_type

  security_groups = [aws_security_group.airlines_sg.name]
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  # User data to install docker, docker-compose and run the app
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo amazon-linux-extras install docker -y
              sudo service docker start
              sudo usermod -a -G docker ec2-user
              
              # Install docker-compose
              sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              sudo chmod +x /usr/local/bin/docker-compose
              
              # Pull the project (In a real scenario, this would be from ECR or a built artifact, here we mock it or clone repo)
              # For this example, let's assume the CI/CD pipeline SSHes into the box and runs docker-compose up,
              # or the user copies the docker-compose.yml over. 
              # As a quick start, we just ensure Docker is ready.
              EOF

  tags = {
    Name = "AirlinesAppServer"
  }
}
