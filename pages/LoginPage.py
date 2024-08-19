import logging
from utils.element_utils import find_element_with_fallback
from pages.ProductListPage import ProductListPage


class LoginPage:

    def __init__(self, page, logger):
        self.page = page
        self.logger = logger
        self._username_locators = [
            ("placeholder", "test"),
            ("id", "user-name")
        ]
        self._password_locators = [
            ("placeholder", "Password"),
            ("id", "password")
        ]
        self._login_btn_locators = [
            ("text", "Login"),
            ("xpath", "//button[contains(text(), 'Login')]")
        ]
        self._error_message_locators = [
            ("data-test", "error"),
            ("xpath", "//div[contains(@class, 'error') and contains(text(), 'sadface')]")
        ]

    def enter_username(self, u_name):
        self.logger.info(f'Entering username: {u_name}')
        username_field = find_element_with_fallback(self.page, self._username_locators, self.logger)
        username_field.clear()
        username_field.fill(u_name)

    def enter_password(self, p_word):
        self.logger.info(f'Entering password: {p_word}')
        password_field = find_element_with_fallback(self.page, self._password_locators, self.logger)
        password_field.clear()
        password_field.fill(p_word)

    def click_login(self):
        self.logger.info('Clicking login button')
        login_button = find_element_with_fallback(self.page, self._login_btn_locators, self.logger)
        login_button.click()

    def do_login(self, credentials, product):
        self.logger.info('Performing login')
        self.enter_username(credentials['username'])
        self.enter_password(credentials['password'])
        self.click_login()
        return ProductListPage(self.page, product, self.logger)

    @property
    def login_button_locator(self):
        return find_element_with_fallback(self.page, self._login_btn_locators, self.logger)