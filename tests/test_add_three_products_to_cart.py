from playwright.sync_api import expect
from pages.LoginPage import LoginPage
from tests.base_test import BaseTest


class TestAddThreeProductsToCart(BaseTest):

    def test_add_three_products_to_cart(self, set_up_tear_down, data):
        data_set_id = data['id']
        self.initialize_logger(data_set_id)

        page = set_up_tear_down
        credentials = self.read_credentials()
        products = [data['product_1'], data['product_2'], data['product_3']]

        try:
            self.logger.info('Starting test: test_add_three_products_to_cart')
            self.logger.info(f"Using user: {credentials['username']}")
            self.logger.info(f'Products: {products}')

            login_p = LoginPage(page, self.logger)
            products_p = login_p.do_login(credentials)
            expect(products_p.product_header).to_have_text("Products")
            self.take_screenshot(page, 'product_list_page', data_set_id)

            self.logger.info('Adding three products to cart')
            expected_item_total = 0.0
            for product in products:
                expected_item_total += products_p.get_product_price(product)
                products_p.add_product_to_cart(product)
                expect(products_p.get_add_remove_cart_locator(product)).to_have_text("Remove")
            expect(products_p.cart_badge).to_have_text("3")
            self.take_screenshot(page, 'added_three_products', data_set_id)

            self.logger.info('Verifying cart contents')
            cart_p = products_p.click_cart_icon()
            expect(cart_p.item_names).to_have_text(products)
            self.take_screenshot(page, 'cart_page', data_set_id)

            self.logger.info('Entering checkout details')
            checkout_p = cart_p.click_checkout_button()
            checkout_p.enter_checkout_details(data['first_name'], data['last_name'], data['zipcode'])
            checkout_p.click_continue()

            self.logger.info('Verifying checkout overview')
            expect(checkout_p.item_names).to_have_text(products)
            expect(checkout_p.item_total).to_have_text(f"Item total: ${expected_item_total:.2f}")
            self.take_screenshot(page, 'checkout_overview', data_set_id)

            self.logger.info('Finishing order')
            checkout_p.click_finish_button()
            expect(checkout_p.get_confirm_message()).to_have_text("Thank you for your order!")
            self.take_screenshot(page, 'checkout_confirmation', data_set_id)
            self.logger.info('Test completed successfully')

        except AssertionError as ae:
            self.fail_test(page, f"Assertion error occurred: {str(ae)}", data_set_id)
        except Exception as e:
            self.fail_test(page, f"Test failed due to an exception: {str(e)}", data_set_id)
        finally:
            self.logger.info('Test finished: test_add_three_products_to_cart')
