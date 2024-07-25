import pytest
from playwright.sync_api import Page, expect
from pytest_playwright_visual.plugin import assert_snapshot
from pages.LoginPage import LoginPage
from tests.base_test import BaseTest
#pytest --update-snapshots


class TestLoginVisual(BaseTest):

    def test_login_visual(self, set_up_tear_down, data,assert_snapshot):
        data_set_id = data['id']
        self.initialize_logger(data_set_id)

        page = set_up_tear_down
        credentials = self.read_credentials()
        product_name = data['product']

        try:
            self.logger.info('Starting test: test_login_visual')
            self.logger.info(f'Using credentials: {credentials}')
            self.logger.info(f'Product name: {product_name}')

            login_p = LoginPage(page, self.logger)
            self.logger.info('Entering username')
            login_p.enter_username(credentials['username'])
            self.take_screenshot(page, 'entered_username', data_set_id)

            self.logger.info('Entering password')
            login_p.enter_password(credentials['password'])
            self.take_screenshot(page, 'entered_password', data_set_id)

            self.logger.info('Clicking login')
            self.take_screenshot(page, 'before_click_login', data_set_id)
            #assert_snapshot(page.screenshot(mask=[login_p.login_button_locator]))
            assert_snapshot(page.screenshot(full_page=True))

        except AssertionError as ae:
            self.fail_test(page, f"Assertion error occurred: {str(ae)}", data_set_id)
        except Exception as e:
            self.fail_test(page, f"Test failed due to an exception: {str(e)}", data_set_id)
        finally:
            self.logger.info('Test finished: test_login_visual')
