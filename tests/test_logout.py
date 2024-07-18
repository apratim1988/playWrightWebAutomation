import re
from playwright.sync_api import Page, expect

from pages.LoginPage import LoginPage



def xtest_logout(set_up_tear_down) -> None:
    page= set_up_tear_down
    credentials= {'username': 'standard_user', 'password': 'secret_sauce'} # masking mechanism
    login_p= LoginPage(page)
    products_p= login_p.do_login(credentials)
    products_p.do_logout()
    expect(login_p.login_button).to_be_visible()