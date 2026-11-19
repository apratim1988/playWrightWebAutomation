
import base64
import os
import pytest
from playwright.sync_api import sync_playwright
from utils.config import Config
from utils.environment_urls import ENVIRONMENT_URLS
from utils.excel_utils import read_test_data

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
    return pytestconfig.getoption("playwright_browser")

@pytest.fixture(scope="session")
def environment(pytestconfig):
    env = pytestconfig.getoption("environment").lower()
    if env in ENVIRONMENT_URLS:
        os.environ['ENVIRONMENT'] = env
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
def set_up_tear_down(request, browser_context, environment):
    page = browser_context.new_page()
    page.set_viewport_size({"width": 1536, "height": 800})
    page.goto(environment)
    # Expose the page to the test instance so the failure hook can screenshot it.
    if request.instance is not None:
        request.instance.page = page
    yield page
    page.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a failure screenshot to the pytest-html report.

    Runs while the report is being built (before pytest-html renders it) and while
    the page is still open, which pytest_exception_interact does not guarantee.
    """
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    instance = item.instance
    page = getattr(instance, 'page', None)
    data_set_id = getattr(instance, 'data_set_id', None)
    if page is None or data_set_id is None or page.is_closed():
        return

    # Reuse the screenshot fail_test already took; otherwise take one now.
    screenshot_path = getattr(instance, 'failure_screenshot', None) or \
        instance.take_screenshot(page, 'failure', data_set_id)

    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html and screenshot_path and os.path.exists(screenshot_path):
        with open(screenshot_path, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
        extras = getattr(report, 'extras', [])
        extras.append(pytest_html.extras.image(encoded, mime_type="image/png", extension="png"))
        report.extras = extras

@pytest.fixture(scope="session")
def test_data_file(environment):
    env_name = [key for key, value in ENVIRONMENT_URLS.items() if value == environment][0]
    return Config.get_excel_file_path(env_name)

def pytest_generate_tests(metafunc):
    if "data" in metafunc.fixturenames:
        env = metafunc.config.getoption("environment").lower()
        file_path = Config.get_excel_file_path(env)
        if not os.path.exists(file_path):
            pytest.exit(f"Test data workbook not found for environment '{env}': {file_path}", returncode=4)
        test_case_name = metafunc.function.__name__
        sheet_name = Config.get_sheet_name(test_case_name)
        test_data = read_test_data(file_path, sheet_name)
        metafunc.parametrize("data", test_data)
