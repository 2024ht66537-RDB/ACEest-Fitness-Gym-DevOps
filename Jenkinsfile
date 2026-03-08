pipeline {
    agent any

    environment {
        IMAGE_NAME = 'aceest-fitness-gym'
        IMAGE_TAG  = 'latest'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '>>> Checking out source code from GitHub...'
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                echo '>>> Setting up Python virtual environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                echo '>>> Running flake8 linter...'
                sh '''
                    . venv/bin/activate
                    flake8 app.py --max-line-length=100 --ignore=E501,W503
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                echo '>>> Running Pytest unit tests...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v --tb=short --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo '>>> Building Docker image...'
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Docker Test') {
            steps {
                echo '>>> Running tests inside Docker container...'
                sh """
                    docker run --rm \
                        --entrypoint pytest \
                        ${IMAGE_NAME}:${IMAGE_TAG} \
                        tests/ -v --tb=short
                """
            }
        }
    }

    post {
        success {
            echo '✅ BUILD SUCCESSFUL — All stages passed!'
        }
        failure {
            echo '❌ BUILD FAILED — Check the logs above.'
        }
        always {
            echo '>>> Cleaning up workspace...'
            sh 'rm -rf venv || true'
        }
    }
}
