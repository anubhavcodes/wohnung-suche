#!groovy
def deployServices (services = '') {
  checkout scm
  sh "./scripts/run-deploy"
}

stage('Deploy to Production') {
    try {
        node ('production') {
            deployServices()
        }
    } catch (Exception e) {
    throw e
    }
}
