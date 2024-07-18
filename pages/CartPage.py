from pages.CheckoutPage import CheckoutPage

class CartPage:

    def __init__(self, page, logger):
        self.page = page
        self.logger = logger
        self.checkout_button = page.locator("//button[@id='checkout']")

    def click_checkout_button(self):
        self.logger.info('Clicking checkout button')
        self.checkout_button.click()
        return CheckoutPage(self.page, self.logger)
