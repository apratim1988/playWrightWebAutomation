import pytest
from playwright.sync_api import sync_playwright
from utils.config import Config
from py.xml import html

@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as playwright_instance:
        yield playwright_instance

@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=True)  # Set headless=True for headless mode
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def browser_context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="function")
def set_up_tear_down(browser_context):
    page = browser_context.new_page()
    page.set_viewport_size({"width": 1536, "height": 800})
    page.goto("https://www.saucedemo.com/")
    yield page
    page.close()


import pytest
from py.xml import html

import pytest
from py.xml import html

@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(node, call, report):
    if report.failed:
        base_test_instance = node.instance
        page = getattr(base_test_instance, 'page', None)
        data_set_id = getattr(base_test_instance, 'data_set_id', None)

        print("Debug: Test failed, trying to capture screenshot...")  # Debug print

        if page and data_set_id:
            step_name = 'failure'
            screenshot_path = base_test_instance.take_screenshot(page, step_name, data_set_id)

            print(f"Debug: Screenshot path - {screenshot_path}")  # Debug print

            if screenshot_path:
                extra = getattr(report, 'extra', [])
                extra.append(html.div(html.a(html.img(src=screenshot_path, width='800px'), href=screenshot_path)))
                report.extra = extra
            else:
                print("Debug: Screenshot path not returned or invalid")  # Debug print
        else:
            print("Debug: Page or data_set_id not available")  # Debug print

