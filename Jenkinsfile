pipeline {
    agent any

    stages {
        stage('Generate Jobs') {
            steps {
                jobDsl(
                    targets: 'jenkins/job_dsl.groovy',
                    removedJobAction: 'DELETE',
                    removedViewAction: 'DELETE',
                    lookupStrategy: 'JENKINS_ROOT'
                )
            }
        }
    }
}
