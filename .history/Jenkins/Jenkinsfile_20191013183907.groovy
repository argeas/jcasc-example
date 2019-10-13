pipeline {
    agent any

    stages {
        stage('Run Tests') {
            steps {
                
                script {
              
                    sh """
                    ssh -i /var/jenkins_home/.ssh/id_ed25519_bs debian@172.17.0.1 -p 43453 "ssh -o StrictHostKeyChecking=no -i /home/debian/.ssh/id_ed25519_bs -f -nNT -R 8081:localhost:8081 debian@$PRIVATE_IP -p 43453"
                    """
                           
                          
                }
                // publishHTML([
                //     allowMissing: false,
                //     alwaysLinkToLastBuild: false,
                //     keepAll: true,
                //     reportDir: 'test',
                //     reportFiles: 'test/index.html',
                //     reportName: 'HTML Report',
                //     reportTitles: ''])
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: false,
                    keepAll: true,
                    reportDir: 'test',
                    reportFiles: '/var/jenkins_home/workspace/run-all-e2e-tests/test/index.html',
                    reportName: 'HTML Report'
                ]
            }
        }        
    }
}



