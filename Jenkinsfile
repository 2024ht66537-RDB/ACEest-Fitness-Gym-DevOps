pipeline {
    agent any

    environment {
        IMAGE_NAME = 'aceest-fitness-gym'
        IMAGE_TAG  = 'latest'
        PYTHON = 'C:\\Users\\RishabhDevBhardwaj\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
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
                bat """
                    "%PYTHON%" -m venv venv
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\pip.exe install -r requirements.txt
                """
            }
        }

        stage('Lint') {
            steps {
                echo '>>> Running flake8 linter...'
                bat 'venv\\Scripts\\flake8.exe app.py --max-line-length=100 --ignore=E501,W503,E221,E241'
            }
        }

        stage('Unit Tests') {
            steps {
                echo '>>> Running Pytest unit tests...'
                bat 'venv\\Scripts\\pytest.exe tests/ -v --tb=short --junitxml=test-results.xml'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo '>>> Building Docker image...'
                bat "docker build -t %IMAGE_NAME%:%IMAGE_TAG% ."
            }
        }

        stage('Docker Test') {
            steps {
                echo '>>> Running tests inside Docker container...'
                bat "docker run --rm --entrypoint pytest %IMAGE_NAME%:%IMAGE_TAG% tests/ -v --tb=short"
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
            bat 'if exist venv rmdir /s /q venv'
        }
    }
}