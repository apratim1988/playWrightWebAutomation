import pytest
from playwright.sync_api import sync_playwright
from utils.config import Config
from py.xml import html
from utils.environment_urls import ENVIRONMENT_URLS

def pytest_addoption(parser):
    parser.addoption(
        "--playwright-browser", action="store", default="chromium",
        help="Browser to run tests with: chromium, firefox, or webkit"
    )
    parser.addoption(
        "--environment", action="store", default="production",
        help="Environment to run tests in: production, beta, dev, qa"
    )

@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    return pytestconfig.getoption("playwright-browser")

@pytest.fixture(scope="session")
def environment(pytestconfig):
    env = pytestconfig.getoption("environment").lower()
    if env in ENVIRONMENT_URLS:
        return ENVIRONMENT_URLS[env]
    else:
        raise ValueError(f"Unsupported environment: {env}")

@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as playwright_instance:
        yield playwright_instance

@pytest.fixture(scope="session")
def browser(playwright, browser_name):
    if browser_name == "chromium":
        browser = playwright.chromium.launch(headless=True)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=True)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=True)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def browser_context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="function")
def set_up_tear_down(browser_context, environment):
    page = browser_context.new_page()
    page.set_viewport_size({"width": 1536, "height": 800})
    page.goto(environment)
    yield page
    page.close()

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
