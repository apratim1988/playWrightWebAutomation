import logging
from pages.ProductListPage import ProductListPage


class LoginPage:

    def __init__(self, page, logger):
        self.page = page
        self.logger = logger
        self._username = page.get_by_placeholder("Username")
        self._password = page.get_by_placeholder("Password")
        self._login_btn = page.get_by_text("Login")
        self._error_message = page.locator("//h3[contains(text(), 'Epic sadface')]")

    def enter_username(self, u_name):
        self.logger.info(f'Entering username: {u_name}')
        self._username.clear()
        self._username.fill(u_name)

    def enter_password(self, p_word):
        self.logger.info(f'Entering password: {p_word}')
        self._password.clear()
        self._password.fill(p_word)

    def click_login(self):
        self.logger.info('Clicking login button')
        self._login_btn.click()

    def do_login(self, credentials, product):
        self.logger.info('Performing login')
        self.enter_username(credentials['username'])
        self.enter_password(credentials['password'])
        self.click_login()
        return ProductListPage(self.page, product, self.logger)

    @property
    def login_button_locator(self):
        return self._login_btn
