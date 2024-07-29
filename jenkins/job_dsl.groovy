job('RunTestsForAllEnvironments') {
    description('Runs Playwright tests for all environments')

    scm {
        git('https://your-repository-url.git', 'main')
    }

    triggers {
        scm('H 1 * * *')
    }

    steps {
        def environments = ['production', 'beta', 'dev', 'qa']
        def browsers = ['chromium', 'firefox', 'webkit']

        environments.each { env ->
            def usernameCredentialId = "${env}-username"
            def passwordCredentialId = "${env}-password"

            browsers.each { browser ->
                withCredentials([usernamePassword(credentialsId: usernameCredentialId, usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    shell("""
                        export ENVIRONMENT=${env}
                        export USERNAME=$USERNAME
                        export PASSWORD=$PASSWORD
                        cd tests && py -m pytest -v -s --playwright-browser=${browser} --environment=${env} --html=report/report.html
                    """)
                }
            }
        }
    }

    publishers {
        publishHtml {
            report('tests/report') {
                reportFiles('report.html')
                reportName('Playwright Test Report')
                keepAll()
                allowMissing(false)
                alwaysLinkToLastBuild(true)
            }
        }
    }
}
