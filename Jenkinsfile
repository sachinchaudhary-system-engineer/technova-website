
pipeline {
    agent any

    stages {

        stage("Code Checkout") {
            steps {
                git branch: 'main',
                    url: 'https://github.com/sachinchaudhary-system-engineer/technova-website.git'

                echo "Code checkout completed"
            }
        }

        stage("Build") {
            steps {
                sh '''
                    docker build -t chaudharysachin/technova-frontend:v1 ./frontend
                    docker build -t chaudharysachin/technova-backend:v1 ./backend
                '''

                echo "Docker build completed"
            }
        }

        stage("Push to DockerHub") {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-hub-cred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login \
                            -u "$DOCKER_USER" --password-stdin

                        docker push chaudharysachin/technova-frontend:v1
                        docker push chaudharysachin/technova-backend:v1

                        docker logout
                    '''
                }
            }
        }

        stage("Deploy to Kubernetes") {
            steps {
                sh ''' 

                    kubectl apply -f k8s/ -n website

                    kubectl set image deployment/frontend-deployment \
                        frontend-container=chaudharysachin/technova-frontend:v1 \
                        -n website

                    kubectl set image deployment/backend-deployment \
                        backend-container=chaudharysachin/technova-backend:v1 \
                        -n website
                '''

                echo "Deployment to Kubernetes completed"
            }
        }

        stage("Verify Deployment") {
            steps {
                sh '''
                    echo "Waiting 30 seconds for pods to initialize..."
                    sleep 30

                    cho "Checking Pods..."
                    kubectl get pods -n website

                    echo "Checking Deployments..."
                    kubectl get deployments -n website

                    echo "Checking Services..."
                    kubectl get svc -n website

                    echo "Checking Ingress..."
                    kubectl get ingress -n website

                    echo "Waiting for Backend Deployment..."
                    kubectl rollout status deployment/backend-deployment \
                        -n website --timeout=180s

                    echo "Waiting for Frontend Deployment..."
                    kubectl rollout status deployment/frontend-deployment \
                        -n website --timeout=180s

                    echo "Waiting for Redis Deployment..."
                    kubectl rollout status deployment/redis \
                        -n website --timeout=180s

                    echo "All deployments are ready!"

                    echo "Final Pod Status:"
                    kubectl get pods -n website

                echo "Deployment verification completed"
                '''
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed. Please check the logs for details."
        }

        success {
            echo "Pipeline completed successfully."
        }

        always {
            echo "CI/CD pipeline execution finished."
        }
    }
}
