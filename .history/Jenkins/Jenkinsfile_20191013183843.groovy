pipeline {
    agent any

    parameters {
                string(name: 'PRIVATE_IP', defaultValue: '', description: 'private ip of the droplet passed from the parent job')
    }

    stages {
        stage('Run e2e tests via fabric') {
            steps {
                
                script {
              
                    sh """
                    ssh -i /var/jenkins_home/.ssh/id_ed25519_bs debian@172.17.0.1 -p 43453 "ssh -o StrictHostKeyChecking=no -i /home/debian/.ssh/id_ed25519_bs -f -nNT -R 8081:localhost:8081 debian@$PRIVATE_IP -p 43453"
                    """
                    sh """
                    fab -f $WORKSPACE/terraform/jenkins-build-server/fabfile.py -H $PRIVATE_IP:43453 -u "debian" -i /var/jenkins_home/.ssh/id_ed25519_bs run_moft_tests
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



