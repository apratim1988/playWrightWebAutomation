from urllib.parse import urljoin
from playwright.sync_api import expect
from pages.LoginPage import LoginPage
from tests.base_test import BaseTest

# Not data-driven: these scenarios need no Excel rows, so artifacts use data set 1.
DATA_SET_ID = 1


class TestLogin(BaseTest):

    def test_login_with_valid_user(self, set_up_tear_down):
        self.initialize_logger(DATA_SET_ID)
        page = set_up_tear_down
        credentials = self.read_credentials()

        try:
            self.logger.info('Starting test: test_login_with_valid_user')
            products_p = LoginPage(page, self.logger).do_login(credentials)
            self.take_screenshot(page, 'after_login', DATA_SET_ID)
            expect(products_p.product_header).to_have_text("Products")
        except AssertionError as ae:
            self.fail_test(page, f"Assertion error occurred: {str(ae)}", DATA_SET_ID)
        except Exception as e:
            self.fail_test(page, f"Test failed due to an exception: {str(e)}", DATA_SET_ID)
        finally:
            self.logger.info('Test finished: test_login_with_valid_user')

    def test_login_with_invalid_user(self, set_up_tear_down):
        self.initialize_logger(DATA_SET_ID)
        page = set_up_tear_down
        invalid_credentials = {'username': 'invalid_user', 'password': 'invalid_password'}

        try:
            self.logger.info('Starting test: test_login_with_invalid_user')
            login_p = LoginPage(page, self.logger)
            login_p.do_login(invalid_credentials)
            self.take_screenshot(page, 'after_login', DATA_SET_ID)
            expect(login_p.error_message).to_have_text(
                "Epic sadface: Username and password do not match any user in this service")
        except AssertionError as ae:
            self.fail_test(page, f"Assertion error occurred: {str(ae)}", DATA_SET_ID)
        except Exception as e:
            self.fail_test(page, f"Test failed due to an exception: {str(e)}", DATA_SET_ID)
        finally:
            self.logger.info('Test finished: test_login_with_invalid_user')

    def test_login_with_no_user(self, set_up_tear_down):
        self.initialize_logger(DATA_SET_ID)
        page = set_up_tear_down

        try:
            self.logger.info('Starting test: test_login_with_no_user')
            login_p = LoginPage(page, self.logger)
            login_p.click_login()
            self.take_screenshot(page, 'after_click_login', DATA_SET_ID)
            expect(login_p.error_message).to_have_text("Epic sadface: Username is required")
        except AssertionError as ae:
            self.fail_test(page, f"Assertion error occurred: {str(ae)}", DATA_SET_ID)
        except Exception as e:
            self.fail_test(page, f"Test failed due to an exception: {str(e)}", DATA_SET_ID)
        finally:
            self.logger.info('Test finished: test_login_with_no_user')

    def test_access_inventory_without_login(self, set_up_tear_down):
        self.initialize_logger(DATA_SET_ID)
        page = set_up_tear_down

        try:
            self.logger.info('Starting test: test_access_inventory_without_login')
            page.goto(urljoin(page.url, 'inventory.html'))
            login_p = LoginPage(page, self.logger)
            self.take_screenshot(page, 'after_open_inventory', DATA_SET_ID)
            expect(login_p.error_message).to_have_text(
                "Epic sadface: You can only access '/inventory.html' when you are logged in.")
        except AssertionError as ae:
            self.fail_test(page, f"Assertion error occurred: {str(ae)}", DATA_SET_ID)
        except Exception as e:
            self.fail_test(page, f"Test failed due to an exception: {str(e)}", DATA_SET_ID)
        finally:
            self.logger.info('Test finished: test_access_inventory_without_login')
