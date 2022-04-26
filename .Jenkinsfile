pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                echo 'Hello World'
            }
        }
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/Apfirebolt/Password-Management-App-in-Django']]])
            }
        }
        stage('Build') {
            steps {
                bat label: 'Django Start Script', script: 'C:\\Amit\\Projects\\Django_projects\\venvs\\teacher\\Scripts\\python.exe manage.py runserver'
            }
        }
    }
}
