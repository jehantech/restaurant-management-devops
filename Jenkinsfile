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

        stage('Trivy Security Scan') {
            steps {
                bat '''
            docker save restaurant-management-ci-restaurant-service:latest -o restaurant-service.tar
            docker save restaurant-management-ci-menu-service:latest -o menu-service.tar
            docker save restaurant-management-ci-customer-service:latest -o customer-service.tar
            docker save restaurant-management-ci-order-service:latest -o order-service.tar

            echo ================================
            echo TRIVY - RESTAURANT SERVICE
            echo ================================
            docker run --rm -v trivy-cache:/root/.cache/trivy -v "%CD%:/work" aquasec/trivy:latest image --input /work/restaurant-service.tar --scanners vuln --severity HIGH,CRITICAL --exit-code 0

            echo ================================
            echo TRIVY - MENU SERVICE
            echo ================================
            docker run --rm -v trivy-cache:/root/.cache/trivy -v "%CD%:/work" aquasec/trivy:latest image --input /work/menu-service.tar --scanners vuln --severity HIGH,CRITICAL --exit-code 0

            echo ================================
            echo TRIVY - CUSTOMER SERVICE
            echo ================================
            docker run --rm -v trivy-cache:/root/.cache/trivy -v "%CD%:/work" aquasec/trivy:latest image --input /work/customer-service.tar --scanners vuln --severity HIGH,CRITICAL --exit-code 0

            echo ================================
            echo TRIVY - ORDER SERVICE
            echo ================================
            docker run --rm -v trivy-cache:/root/.cache/trivy -v "%CD%:/work" aquasec/trivy:latest image --input /work/order-service.tar --scanners vuln --severity HIGH,CRITICAL --exit-code 0

            echo ================================
            echo CRITICAL SECURITY GATE
            echo ================================

            docker run --rm -v trivy-cache:/root/.cache/trivy -v "%CD%:/work" aquasec/trivy:latest image --input /work/restaurant-service.tar --scanners vuln --severity CRITICAL --exit-code 1
            docker run --rm -v trivy-cache:/root/.cache/trivy -v "%CD%:/work" aquasec/trivy:latest image --input /work/menu-service.tar --scanners vuln --severity CRITICAL --exit-code 1
            docker run --rm -v trivy-cache:/root/.cache/trivy -v "%CD%:/work" aquasec/trivy:latest image --input /work/customer-service.tar --scanners vuln --severity CRITICAL --exit-code 1
            docker run --rm -v trivy-cache:/root/.cache/trivy -v "%CD%:/work" aquasec/trivy:latest image --input /work/order-service.tar --scanners vuln --severity CRITICAL --exit-code 1

            del /f /q restaurant-service.tar
            del /f /q menu-service.tar
            del /f /q customer-service.tar
            del /f /q order-service.tar
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

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    set KUBECONFIG=C:\\ProgramData\\Jenkins\\.kube\\config

                    kubectl apply -f k8s\\restaurant-service.yaml
                    kubectl apply -f k8s\\menu-service.yaml
                    kubectl apply -f k8s\\customer-service.yaml
                    kubectl apply -f k8s\\order-service.yaml

                    kubectl rollout restart deployment restaurant-service
                    kubectl rollout restart deployment menu-service
                    kubectl rollout restart deployment customer-service
                    kubectl rollout restart deployment order-service
                '''
            }
        }

        stage('Wait for Kubernetes Deployment') {
            steps {
                bat '''
                    set KUBECONFIG=C:\\ProgramData\\Jenkins\\.kube\\config

                    kubectl rollout status deployment/restaurant-service --timeout=120s
                    kubectl rollout status deployment/menu-service --timeout=120s
                    kubectl rollout status deployment/customer-service --timeout=120s
                    kubectl rollout status deployment/order-service --timeout=120s
                '''
            }
        }

        stage('Check Kubernetes Services') {
            steps {
                bat '''
                    set KUBECONFIG=C:\\ProgramData\\Jenkins\\.kube\\config

                    kubectl get deployments
                    kubectl get services
                    kubectl get pods -l "app in (restaurant-service,menu-service,customer-service,order-service)"
                '''
            }
        }

        stage('Start Application Port Forwarding') {
            steps {
                bat '''
                    set KUBECONFIG=C:\\ProgramData\\Jenkins\\.kube\\config

                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$env:KUBECONFIG='C:\\ProgramData\\Jenkins\\.kube\\config'; Start-Process powershell -ArgumentList '-NoProfile','-Command','kubectl port-forward service/restaurant-service 8001:8001' -WindowStyle Hidden; Start-Process powershell -ArgumentList '-NoProfile','-Command','kubectl port-forward service/menu-service 8002:8002' -WindowStyle Hidden; Start-Process powershell -ArgumentList '-NoProfile','-Command','kubectl port-forward service/customer-service 8003:8003' -WindowStyle Hidden; Start-Process powershell -ArgumentList '-NoProfile','-Command','kubectl port-forward service/order-service 8004:8004' -WindowStyle Hidden"
                '''
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