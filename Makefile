# Makefile for Airlines-Project

.PHONY: build up down deploy-aws terraform-init terraform-apply terraform-destroy

# Local Development
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

# AWS Deployment
terraform-init:
	cd terraform && terraform init

terraform-plan:
	cd terraform && terraform plan

terraform-apply:
	cd terraform && terraform apply -auto-approve

terraform-destroy:
	cd terraform && terraform destroy -auto-approve

deploy-aws: terraform-init terraform-apply
