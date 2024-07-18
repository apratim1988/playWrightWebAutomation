from pages.CartPage import CartPage

class ProductListPage:

    def __init__(self, page, product, logger):
        self.page = page
        self.product = product
        self.logger = logger
        self._products_header = page.locator("span.title")
        self._burger_menu = page.locator("//button[@id='react-burger-menu-btn']")
        self._logout_btn = page.locator("//a[@data-test='logout-sidebar-link']")
        self._add_to_cart = page.locator(f"//div[text()='{product}']/ancestor::div[@class='inventory_item_label']/following-sibling::div/button")
        self._cart_icon = page.locator("//a[@class='shopping_cart_link']")

    @property
    def product_header(self):
        self.logger.info('Getting product header')
        return self._products_header

    def click_burger_menu_btn(self):
        self.logger.info('Clicking burger menu button')
        self._burger_menu.click()

    def click_logout(self):
        self.logger.info('Clicking logout button')
        self._logout_btn.click()

    def do_logout(self):
        self.logger.info('Performing logout')
        self.click_burger_menu_btn()
        self.click_logout()

    def get_add_remove_cart_locator(self, product):
        self.logger.info(f'Getting add/remove cart locator for product: {product}')
        return self.page.locator(f"//div[text()='{product}']/ancestor::div[@class='inventory_item_label']/following-sibling::div/button")

    def click_add_to_cart_or_remove(self):
        self.logger.info('Clicking add to cart or remove button')
        self._add_to_cart.click()
        return self

    def click_cart_icon(self):
        self.logger.info('Clicking cart icon')
        self._cart_icon.click()
        return CartPage(self.page, self.logger)
