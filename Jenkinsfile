pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment Check') {
            steps {
                bat 'git --version'
                bat 'python --version'
                bat 'docker --version'
                bat '"C:\\Users\\jehan\\AppData\\Local\\Programs\\DockerDesktop\\resources\\cli-plugins\\docker-compose.exe" version'
            }
        }

        stage('Test Restaurant Service') {
            steps {
                dir('restaurant-service') {
                    bat '''
                        if not exist data mkdir data
                        python -m pip install -r requirements.txt
                        python -m pytest -v
                    '''
                }
            }
        }

        stage('Test Menu Service') {
            steps {
                dir('menu-service') {
                    bat '''
                        if not exist data mkdir data
                        python -m pip install -r requirements.txt
                        python -m pytest -v
                    '''
                }
            }
        }

        stage('Test Customer Service') {
            steps {
                dir('customer-service') {
                    bat '''
                        if not exist data mkdir data
                        python -m pip install -r requirements.txt
                        python -m pytest -v
                    '''
                }
            }
        }

        stage('Test Order Service') {
            steps {
                dir('order-service') {
                    bat '''
                        if not exist data mkdir data
                        python -m pip install -r requirements.txt
                        python -m pytest -v
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                bat '"C:\\Users\\jehan\\AppData\\Local\\Programs\\DockerDesktop\\resources\\cli-plugins\\docker-compose.exe" -f docker-compose.yml build'
            }
        }

        stage('Deploy') {
            steps {
                bat '"C:\\Users\\jehan\\AppData\\Local\\Programs\\DockerDesktop\\resources\\cli-plugins\\docker-compose.exe" -p restaurant-management -f docker-compose.yml up -d'
            }
        }

        stage('Check Services') {
            steps {
                bat '"C:\\Users\\jehan\\AppData\\Local\\Programs\\DockerDesktop\\resources\\cli-plugins\\docker-compose.exe" -p restaurant-management -f docker-compose.yml ps'
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
    }
}