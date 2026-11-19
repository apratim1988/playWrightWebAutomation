class CheckoutPage:

    def __init__(self, page, logger):
        self.page = page
        self.logger = logger
        self._first_name = page.locator("//input[@id='first-name']")
        self._last_name = page.locator("//input[@id='last-name']")
        self._zipcode = page.locator("//input[@id='postal-code']")
        self._continue = page.locator("//input[@id='continue']")
        self._finish_button = page.locator("#finish")
        self._confirm_message = page.locator("h2.complete-header")
        self._item_names = page.locator('[data-test="inventory-item-name"]')
        self._item_total = page.locator('[data-test="subtotal-label"]')

    @property
    def item_names(self):
        """Product names listed on the checkout overview (step two)."""
        self.logger.info('Getting overview item names')
        return self._item_names

    @property
    def item_total(self):
        """'Item total: $X' label on the checkout overview (step two)."""
        self.logger.info('Getting item total')
        return self._item_total

    def enter_first_name(self, f_name):
        self.logger.info(f'Entering first name: {f_name}')
        self._first_name.fill(f_name)
        return self

    def enter_last_name(self, l_name):
        self.logger.info(f'Entering last name: {l_name}')
        self._last_name.fill(l_name)
        return self

    def enter_zipcode(self, zip_code):
        self.logger.info(f'Entering zipcode: {zip_code}')
        self._zipcode.fill(str(zip_code))  # Ensure zip code is a string
        return self

    def enter_checkout_details(self, f_name, l_name, zip_code):
        self.logger.info('Entering checkout details')
        self.enter_first_name(f_name).\
            enter_last_name(l_name).\
            enter_zipcode(zip_code)
        return self

    def click_continue(self):
        self.logger.info('Clicking continue')
        self._continue.click()
        return self

    def click_finish_button(self):
        self.logger.info('Clicking finish button')
        self._finish_button.click()
        return self

    def get_confirm_message(self):
        self.logger.info('Getting confirmation message')
        return self._confirm_message
