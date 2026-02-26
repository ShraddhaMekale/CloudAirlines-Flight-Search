# CloudAirlines DevOps Project

A simple 3-tier-style airlines application built to demonstrate core DevOps practices including containerization (Docker), Infrastructure as Code (Terraform), and CI/CD (GitHub Actions) deployed onto AWS.

## Architecture

- **Frontend:** A responsive HTML/CSS/JS application served by NGINX.
- **Backend:** A Python FastAPI REST service returning flight data.
- **Infrastructure (AWS):** An EC2 instance running Docker, provisioned via Terraform, fronted by an AWS Security Group.
- **CI/CD:** GitHub Actions pipeline to test builds and apply Terraform configurations.

## Local Development

### Prerequisites
- Docker and Docker Compose

### Running locally
1. Clone the repository.
2. Navigate to the project root.
3. Run `docker-compose up --build -d`
4. Access the web app at [http://localhost](http://localhost)
5. Access the API at [http://localhost:8000/api/flights](http://localhost:8000/api/flights)

## Deployment (AWS Cloud)

### Prerequisites
- Terraform CLI installed
- AWS CLI configured with proper IAM credentials

### Provisioning Infrastructure
1. Navigate to the `terraform` directory:
   ```bash
   cd terraform
   ```
2. Initialize Terraform:
   ```bash
   terraform init
   ```
3. Apply the configuration to provision the AWS resources:
   ```bash
   terraform apply
   ```
   *Type `yes` when prompted.*
4. Retrieve the output `public_ip` or `website_url` to access your new EC2 instance.

### CI/CD Pipeline
The project includes a `.github/workflows/deploy.yml` which automatically builds the Docker images and applies the Terraform configuration upon a push to the `main` branch. 

**Note:** You must configure `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in your GitHub repository secrets for the pipeline to interact with your AWS account.
# Updated at Thu Feb 26 05:05:59 PM IST 2026
