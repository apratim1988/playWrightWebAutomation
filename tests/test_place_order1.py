import pytest
from playwright.sync_api import Page, expect
from pages.LoginPage import LoginPage
from tests.base_test import BaseTest


class TestPlaceOrder1(BaseTest):

    def test_place_order1(self, set_up_tear_down, data):
        data_set_id = data['id']
        self.initialize_logger(data_set_id)

        page = set_up_tear_down
        credentials = self.read_credentials()
        product_name = data['product']

        try:
            self.logger.info('Starting test: test_place_order1')
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
            products_p = login_p.do_login(credentials, product_name)

            self.logger.info('Adding product to cart')
            self.take_screenshot(page, 'product_list_page', data_set_id)
            products_p.get_add_remove_cart_locator(product_name)
            products_p.click_add_to_cart_or_remove()
            self.take_screenshot(page, 'added_product_to_cart', data_set_id)

            self.logger.info('Navigating to cart')
            checkout_p = products_p.click_cart_icon()
            self.take_screenshot(page, 'cart_page', data_set_id)

            self.logger.info('Proceeding to checkout')
            checkout_p = checkout_p.click_checkout_button()
            self.take_screenshot(page, 'checkout_page', data_set_id)

            self.logger.info('Entering checkout details')
            checkout_p.enter_checkout_details(data['first_name'], data['last_name'], data['zipcode'])
            self.take_screenshot(page, 'entered_checkout_details', data_set_id)

            self.logger.info('Clicking continue')
            checkout_p.click_continue()
            self.take_screenshot(page, 'before_click_finish', data_set_id)

            self.logger.info('Clicking finish')
            checkout_p.click_finish_button()
            self.take_screenshot(page, 'after_click_finish', data_set_id)

            self.logger.info('Verifying order confirmation')
            self.take_screenshot(page, 'checkout_confirmation', data_set_id)
            expect(checkout_p.get_confirm_message()).to_have_text("Thank you for your order!")
            self.logger.info('Test completed successfully')

        except AssertionError as ae:
            self.fail_test(page, f"Assertion error occurred: {str(ae)}", data_set_id)
        except Exception as e:
            self.fail_test(page, f"Test failed due to an exception: {str(e)}", data_set_id)
        finally:
            self.logger.info('Test finished: test_place_order1')