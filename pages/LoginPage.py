import logging
from utils.element_utils import find_element_with_fallback
from pages.ProductListPage import ProductListPage


class LoginPage:

    def __init__(self, page, logger):
        self.page = page
        self.logger = logger
        self._username_locators = [
            ("placeholder", "Username"),
            ("id", "user-name")
        ]
        self._password_locators = [
            ("placeholder", "Password"),
            ("id", "password")
        ]
        self._login_btn_locators = [
            ("data-test", "login-button"),
            ("id", "login-button")
        ]
        # Plain locator (not a fallback list): the error appears only after an action,
        # and find_element_with_fallback checks visibility once without waiting.
        self._error_message = page.locator('[data-test="error"]')
        self._login_button = page.locator('[data-test="login-button"]')

    def enter_username(self, u_name):
        self.logger.info(f'Entering username: {u_name}')
        username_field = find_element_with_fallback(self.page, self._username_locators, self.logger)
        username_field.clear()
        username_field.fill(u_name)

    def enter_password(self, p_word):
        self.logger.info('Entering password: ****')
        password_field = find_element_with_fallback(self.page, self._password_locators, self.logger)
        password_field.clear()
        password_field.fill(p_word)

    def click_login(self):
        self.logger.info('Clicking login button')
        login_button = find_element_with_fallback(self.page, self._login_btn_locators, self.logger)
        login_button.click()

    def do_login(self, credentials, product=None):
        self.logger.info('Performing login')
        self.enter_username(credentials['username'])
        self.enter_password(credentials['password'])
        self.click_login()
        return ProductListPage(self.page, product, self.logger)

    @property
    def login_button_locator(self):
        return find_element_with_fallback(self.page, self._login_btn_locators, self.logger)

    @property
    def login_button(self):
        """Plain locator for expect() checks, e.g. after logout navigates back here."""
        return self._login_button

    @property
    def error_message(self):
        self.logger.info('Getting login error message')
        return self._error_message
