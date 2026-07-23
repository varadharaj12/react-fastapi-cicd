pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        AWS_ACCOUNT_ID = "639962671485"

        BACKEND_REPO = "fastapi-backend"
        FRONTEND_REPO = "react-frontend"

        DEV_SERVER = "13.203.57.158"
        PROD_SERVER = "65.2.212.126"
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
                ssh -o StrictHostKeyChecking=no ubuntu@$DEV_SERVER "bash ~/deploy.sh"
                '''
            }
        }

        stage('Development Health Check') {
            steps {
                sh '''
                ssh -o StrictHostKeyChecking=no ubuntu@$DEV_SERVER \
                "curl -f http://localhost:8000/health"
                '''
            }
        }

        stage('Manual Approval') {
            steps {
                input(
                    message: 'Deploy to Production?',
                    ok: 'Deploy'
                )
            }
        }

        stage('Deploy to Production') {
            steps {
                sh '''
                ssh -o StrictHostKeyChecking=no ubuntu@$PROD_SERVER "bash ~/deploy.sh"
                '''
            }
        }

        stage('Production Health Check') {
            steps {
                sh '''
                ssh -o StrictHostKeyChecking=no ubuntu@$PROD_SERVER \
                "curl -f http://localhost:8000/health"
                '''
            }
        }

    }

    post {

        success {
            echo '==========================================='
            echo 'CI/CD Pipeline Completed Successfully'
            echo '✔ Images Built'
            echo '✔ Images Pushed to Amazon ECR'
            echo '✔ Development Deployment Successful'
            echo '✔ Development Health Check Passed'
            echo '✔ Production Deployment Successful'
            echo '✔ Production Health Check Passed'
            echo '==========================================='
        }

        failure {
            echo '==========================================='
            echo 'Pipeline Failed'
            echo 'Please check Jenkins Console Output'
            echo '==========================================='
        }

        always {
            cleanWs()
        }
    }
}
