pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        AWS_DEFAULT_REGION = 'us-east-1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Containers') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Terraform Plan') {
            steps {
                dir('terraform') {
                    sh 'terraform init'
                    sh 'terraform plan -var="aws_region=us-east-1"'
                }
            }
        }

        stage('Deploy Infrastructure') {
            steps {
                dir('terraform') {
                    sh 'terraform apply -auto-approve -var="aws_region=us-east-1"'
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                dir('terraform') {
                    sh 'terraform output website_url'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
