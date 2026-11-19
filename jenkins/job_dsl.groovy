
def environments = ['production', 'beta', 'dev', 'qa']
def browsers = ['chromium', 'firefox', 'webkit']

environments.each { env ->
    job("RunTestsFor${env.capitalize()}") {
        description("Runs Playwright tests for the ${env} environment")

        scm {
            git('https://your-repository-url.git', 'main')
        }

        triggers {
            scm('H 1 * * *')
        }

        steps {
            browsers.each { browser ->
                def usernameCredentialId = "${env}-username"
                def passwordCredentialId = "${env}-password"

                // The binding exports TEST_USERNAME/TEST_PASSWORD, which BaseTest.read_credentials
                // reads before falling back to the (git-ignored) utils/credentials.json.
                withCredentials([usernamePassword(credentialsId: usernameCredentialId, usernameVariable: 'TEST_USERNAME', passwordVariable: 'TEST_PASSWORD')]) {
                    shell("""
                        export ENVIRONMENT=${env}
                        cd tests && py -m pytest -v -s --playwright-browser=${browser} --environment=${env} --html=report/report.html
                    """)
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
}
