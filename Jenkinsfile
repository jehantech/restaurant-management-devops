pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test Restaurant Service') {
            steps {
                dir('restaurant-service') {
                    bat '''
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
                        python -m pip install -r requirements.txt
                        python -m pytest -v
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'All microservice tests passed successfully!'
        }

        failure {
            echo 'One or more stages failed.'
        }
    }
}