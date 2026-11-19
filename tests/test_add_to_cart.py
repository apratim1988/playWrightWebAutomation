from playwright.sync_api import expect
from pages.LoginPage import LoginPage
from tests.base_test import BaseTest

# Not data-driven: these scenarios need no Excel rows, so artifacts use data set 1.
DATA_SET_ID = 1
PRODUCT_NAME = "Sauce Labs Backpack"


class TestAddToCart(BaseTest):

    def test_add_to_cart(self, set_up_tear_down):
        self.initialize_logger(DATA_SET_ID)
        page = set_up_tear_down
        credentials = self.read_credentials()

        try:
            self.logger.info('Starting test: test_add_to_cart')
            products_p = LoginPage(page, self.logger).do_login(credentials, PRODUCT_NAME)
            products_p.click_add_to_cart_or_remove()
            self.take_screenshot(page, 'added_product_to_cart', DATA_SET_ID)
            expect(products_p.get_add_remove_cart_locator(PRODUCT_NAME)).to_have_text("Remove")
            expect(products_p.cart_badge).to_have_text("1")
        except AssertionError as ae:
            self.fail_test(page, f"Assertion error occurred: {str(ae)}", DATA_SET_ID)
        except Exception as e:
            self.fail_test(page, f"Test failed due to an exception: {str(e)}", DATA_SET_ID)
        finally:
            self.logger.info('Test finished: test_add_to_cart')

    def test_remove_product_from_cart(self, set_up_tear_down):
        self.initialize_logger(DATA_SET_ID)
        page = set_up_tear_down
        credentials = self.read_credentials()

        try:
            self.logger.info('Starting test: test_remove_product_from_cart')
            products_p = LoginPage(page, self.logger).do_login(credentials, PRODUCT_NAME)
            products_p.click_add_to_cart_or_remove()
            expect(products_p.cart_badge).to_have_text("1")
            products_p.click_add_to_cart_or_remove()
            self.take_screenshot(page, 'removed_product_from_cart', DATA_SET_ID)
            expect(products_p.get_add_remove_cart_locator(PRODUCT_NAME)).to_have_text("Add to cart")
            expect(products_p.cart_badge).to_be_hidden()
        except AssertionError as ae:
            self.fail_test(page, f"Assertion error occurred: {str(ae)}", DATA_SET_ID)
        except Exception as e:
            self.fail_test(page, f"Test failed due to an exception: {str(e)}", DATA_SET_ID)
        finally:
            self.logger.info('Test finished: test_remove_product_from_cart')
