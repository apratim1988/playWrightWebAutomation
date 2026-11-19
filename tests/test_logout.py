from playwright.sync_api import expect
from pages.LoginPage import LoginPage
from tests.base_test import BaseTest

# Not data-driven: this scenario needs no Excel rows, so artifacts use data set 1.
DATA_SET_ID = 1


class TestLogout(BaseTest):

    def test_logout(self, set_up_tear_down):
        self.initialize_logger(DATA_SET_ID)
        page = set_up_tear_down
        credentials = self.read_credentials()

        try:
            self.logger.info('Starting test: test_logout')
            login_p = LoginPage(page, self.logger)
            products_p = login_p.do_login(credentials)
            expect(products_p.product_header).to_have_text("Products")
            self.take_screenshot(page, 'after_login', DATA_SET_ID)

            products_p.do_logout()
            self.take_screenshot(page, 'after_logout', DATA_SET_ID)
            expect(login_p.login_button).to_be_visible()
        except AssertionError as ae:
            self.fail_test(page, f"Assertion error occurred: {str(ae)}", DATA_SET_ID)
        except Exception as e:
            self.fail_test(page, f"Test failed due to an exception: {str(e)}", DATA_SET_ID)
        finally:
            self.logger.info('Test finished: test_logout')
