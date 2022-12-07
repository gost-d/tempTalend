node {

    stage('Checkout') {
        checkout scm 
    }
    
    stage('Copy Talend Remote Engine files and docker images ') {
        
        withCredentials([usernamePassword(credentialsId: 'nexus_user', usernameVariable: 'nexus_username', passwordVariable: 'nexus_password')]) {
            sh('curl -u "$nexus_username:$nexus_password" -o "./Talend-RemoteEngine-V${tre_version}.zip" "http://172.22.6.131:8081/repository/devops/talend_remote_engine/v/${tre_version}/v-${tre_version}.zip" ')
            sh('docker login -u $nexus_username -p $nexus_password http://172.22.6.131:8083')
            sh('docker pull 172.22.6.131:8083/devops/ansible:1.0')
            sh('docker pull 172.22.6.131:8083/devops/python:1.1')
        }
    }
    
    stage('Create infrastructure') {
 
        wrap([$class: 'BuildUser']) {
            withCredentials([azureServicePrincipal("azure${env.BUILD_USER_ID}")]) {
                if (params.ostype == 'windows') {
                    sh('docker run -v /home/jenkins/jenkins_home/workspace/Talend_Test:/home/ansible --env AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID --env AZURE_CLIENT_ID=$AZURE_CLIENT_ID --env AZURE_SECRET=$AZURE_CLIENT_SECRET --env AZURE_TENANT=$AZURE_TENANT_ID --rm --rm 172.22.6.131:8083/devops/ansible:1.0  ansible-playbook -vvv /home/ansible/${ostype}/createVM.yaml')
                } else {
                    sh('echo "yes" | ssh-keygen -q -t rsa -N "" -f ./id_rsa')
                    sh('docker run -v /home/jenkins/jenkins_home/workspace/Talend_Test:/home/ansible --env AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID --env AZURE_CLIENT_ID=$AZURE_CLIENT_ID --env AZURE_SECRET=$AZURE_CLIENT_SECRET --env AZURE_TENANT=$AZURE_TENANT_ID --rm --rm 172.22.6.131:8083/devops/ansible:1.0  ansible-playbook -vvv /home/ansible/${ostype}/createVM.yaml')
                }
            }
        }
    }

} 
