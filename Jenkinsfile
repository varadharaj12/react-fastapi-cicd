pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend Docker Image') {
            steps {
                sh 'docker build -t fastapi-backend ./backend'
            }
        }

        stage('Build Frontend Docker Image') {
            steps {
                sh 'docker build -t react-frontend ./frontend'
            }
        }

    }

    post {
        success {
            echo 'Docker Images Built Successfully'
        }

        failure {
            echo 'Pipeline Failed'
        }
    }
}
