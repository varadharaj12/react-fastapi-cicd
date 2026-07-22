pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        AWS_ACCOUNT_ID = "639962671485"

        BACKEND_REPO = "fastapi-backend"
        FRONTEND_REPO = "react-frontend"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend') {
            steps {
                sh 'docker build -t fastapi-backend ./backend'
            }
        }

        stage('Build Frontend') {
            steps {
                sh 'docker build -t react-frontend ./frontend'
            }
        }

        stage('Login to Amazon ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region $AWS_REGION | \
                docker login --username AWS --password-stdin \
                $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                '''
            }
        }

        stage('Tag Images') {
            steps {
                sh '''
                docker tag fastapi-backend:latest \
                $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$BACKEND_REPO:latest

                docker tag react-frontend:latest \
                $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$FRONTEND_REPO:latest
                '''
            }
        }

        stage('Push Images to ECR') {
            steps {
                sh '''
                docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$BACKEND_REPO:latest

                docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$FRONTEND_REPO:latest
                '''
            }
        }

        stage('Deploy to Development') {
            steps {
                sh '''
                ssh -o StrictHostKeyChecking=no ubuntu@13.203.57.158 "bash ~/deploy.sh"
                '''
            }
        }

    }

    post {
        success {
            echo 'Docker Images Built, Pushed to Amazon ECR, and Deployed Successfully'
        }

        failure {
            echo 'Pipeline Failed'
        }
    }
}
