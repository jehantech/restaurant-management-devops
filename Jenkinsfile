pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = 'murakan001'
        DOCKERHUB_TOKEN = credentials('dockerhub-token')
    }

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
                        if exist data\\restaurant.db del /f /q data\\restaurant.db
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
                        if exist data\\menu.db del /f /q data\\menu.db
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
                        if exist data\\customer.db del /f /q data\\customer.db
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
                        if exist data\\order.db del /f /q data\\order.db
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

        stage('Docker Auth Diagnostics') {
            steps {
                bat '''
                    echo Jenkins user:
                    whoami

                    echo.
                    echo Docker context:
                    docker context show

                    echo.
                    echo Docker version:
                    docker version

                    echo.
                    echo Token length:
                    powershell -NoProfile -Command "$env:DOCKERHUB_TOKEN.Length"
                '''
            }
        }

        stage('Docker Hub Login') {
            steps {
                bat '''
                    powershell -NoProfile -NonInteractive -Command "$env:DOCKERHUB_TOKEN | docker login -u $env:DOCKERHUB_USERNAME --password-stdin"
                '''
            }
        }

        stage('Push Images to Docker Hub') {
             steps {
                 bat '''
                    docker tag restaurant-management-ci-restaurant-service:latest %DOCKERHUB_USERNAME%/restaurant-service:latest
                    docker tag restaurant-management-ci-menu-service:latest %DOCKERHUB_USERNAME%/menu-service:latest
                    docker tag restaurant-management-ci-customer-service:latest %DOCKERHUB_USERNAME%/customer-service:latest
                    docker tag restaurant-management-ci-order-service:latest %DOCKERHUB_USERNAME%/order-service:latest

                    docker push %DOCKERHUB_USERNAME%/restaurant-service:latest
                    docker push %DOCKERHUB_USERNAME%/menu-service:latest
                    docker push %DOCKERHUB_USERNAME%/customer-service:latest
                    docker push %DOCKERHUB_USERNAME%/order-service:latest
                 '''
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