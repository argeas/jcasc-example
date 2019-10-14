pipeline {
    agent any
        stages {
            stage('Run Tests') {                
                steps {
                    dir ('testcases') {
                    
                    script {
                        
                        sh"""pipenv install && pipenv run pytest -s test_characters_json_validator.py
                        """                                          
                    }
                }        
            }
        }
    }
}
