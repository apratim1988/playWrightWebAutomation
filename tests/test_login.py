import re
from playwright.sync_api import Page, expect
from pages.LoginPage import LoginPage


def xtest_login_with_standard_user(set_up_tear_down) -> None:
    page= set_up_tear_down
    credentials= {'username': 'standard_user', 'password': 'secret_sauce'} # masking mechanism
    login_p= LoginPage(page)
    products_p= login_p.do_login(credentials)
    expect(products_p.product_header).to_be_visible()
    expect(products_p.product_header).to_have_text("Products")


def xtest_login_with_invalid_user(set_up_tear_down) -> None:
    page = set_up_tear_down
    credentials = {'username': 'invaliduser', 'password': 'invaliduserpassword'}  # masking mechanism
    login_p = LoginPage(page)
    login_p.do_login(credentials)
    expected_fail_message = "Epic sadface: Username and password do not match any user in this service"
    expect(login_p.err_msg_loc).to_contain_text(expected_fail_message)


def xtest_login_with_no_user(set_up_tear_down) -> None:
    page = set_up_tear_down
    login_p = LoginPage(page)
    login_p.click_login()
    expected_fail_message = "Epic sadface: Username is required"
    expect(login_p.err_msg_loc).to_contain_text(expected_fail_message)


def xtest_access_inventory_without_login(set_up_tear_down) -> None:
    page = set_up_tear_down




