import re
from playwright.sync_api import Page, expect
from pages.LoginPage import LoginPage


def xtest_add_to_cart(set_up_tear_down) -> None:
    page= set_up_tear_down
    credentials= {'username': 'standard_user', 'password': 'secret_sauce'} # masking mechanism
    login_p= LoginPage(page)
    products_p= login_p.do_login(credentials)
    product_name= "Sauce Labs Backpack"
    products_p.get_add_remove_cart_loacator(product_name)
    products_p.click_add_to_cart_or_remove(product_name)
    expect(products_p.get_add_remove_cart_loacator(product_name)).to_have_text("Remove")


def xtest_remove_product_from_cart(set_up_tear_down) -> None:
    page= set_up_tear_down
    credentials= {'username': 'standard_user', 'password': 'secret_sauce'} # masking mechanism
    login_p= LoginPage(page)
    products_p= login_p.do_login(credentials)
    product_name= "Sauce Labs Backpack"
    products_p.get_add_remove_cart_loacator(product_name)
    products_p.click_add_to_cart_or_remove(product_name)
    products_p.click_add_to_cart_or_remove(product_name)
    expect(products_p.get_add_remove_cart_loacator(product_name)).to_have_text("Add to cart")