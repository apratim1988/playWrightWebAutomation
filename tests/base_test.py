import pytest
import os
import json
import shutil
from playwright.sync_api import Page, Locator, Route, Request
from utils.config import Config
from utils.logger_utils import setup_logger
from utils.screenshot_utils import capture_screenshot


@pytest.mark.usefixtures("set_up_tear_down")
class BaseTest:
    @classmethod
    def setup_class(cls):
        Config.ensure_directories()
        # Method names whose old artifacts were already cleared in this class.
        cls._cleared_methods = set()

    @classmethod
    def clear_screenshot_for_method(cls, method_name, environment):
        screenshot_dir = os.path.join(Config.SCREENSHOT_DIR, environment, method_name)
        if os.path.exists(screenshot_dir):
            shutil.rmtree(screenshot_dir)

    @classmethod
    def clear_logs_for_method(cls, method_name, environment):
        log_dir = os.path.join(Config.LOG_DIR, environment, method_name)
        if os.path.exists(log_dir):
            shutil.rmtree(log_dir)

    def setup_method(self, method):
        Config.ensure_directories()
        self.method_name = method.__name__
        self.failure_screenshot = None

        # Clear old artifacts once per test method (not once per class), so each
        # method's first data set starts from clean folders.
        if self.method_name not in self.__class__._cleared_methods:
            environment = os.getenv('ENVIRONMENT', 'default')
            if environment == 'default':
                print("Debug: Environment variable not set, using default")
            self.clear_screenshot_for_method(self.method_name, environment)
            self.clear_logs_for_method(self.method_name, environment)
            self.__class__._cleared_methods.add(self.method_name)

    def initialize_logger(self, data_set_id):
        self.data_set_id = data_set_id
        self.logger = setup_logger(self.method_name, self.data_set_id)

    def take_screenshot(self, page, step_name, data_set_id):
        return capture_screenshot(page, self.method_name, step_name, data_set_id)

    def fail_test(self, page, error_message, data_set_id):
        self.logger.error(error_message, exc_info=True)
        self.failure_screenshot = self.take_screenshot(page, 'error', data_set_id)
        pytest.fail(error_message, pytrace=False)

    @staticmethod
    def read_credentials():
        """Return {'username', 'password'} for the current ENVIRONMENT.

        TEST_USERNAME / TEST_PASSWORD environment variables (set by Jenkins) take
        precedence; otherwise the local, git-ignored utils/credentials.json is used.
        """
        environment = os.getenv('ENVIRONMENT')
        if not environment:
            raise EnvironmentError("ENVIRONMENT variable is not set.")

        env_username = os.getenv('TEST_USERNAME')
        env_password = os.getenv('TEST_PASSWORD')
        if env_username and env_password:
            return {'username': env_username, 'password': env_password}

        if not os.path.exists(Config.CREDENTIALS_FILE_PATH):
            raise FileNotFoundError(
                "No credentials: set TEST_USERNAME/TEST_PASSWORD or create "
                f"{Config.CREDENTIALS_FILE_PATH}")

        with open(Config.CREDENTIALS_FILE_PATH, 'r') as file:
            all_credentials = json.load(file)

        credentials = all_credentials.get(environment)
        if not credentials:
            raise KeyError(f"No credentials found for environment: {environment}")

        if not isinstance(credentials, dict) or 'username' not in credentials or 'password' not in credentials:
            raise ValueError(f"Invalid credentials format for environment: {environment}")

        return credentials

    def get_frame_locator(self, page: Page, frame_selector: str):
        """Returns a FrameLocator for the specified iframe selector."""
        return page.frame_locator(frame_selector)

    def select_dropdown_option(self, locator: Locator, option: str):
        """Selects an option from a dropdown."""
        locator.select_option(value=option)

    def check_checkbox(self, locator: Locator, should_check: bool):
        """Checks or unchecks a checkbox based on should_check flag."""
        if should_check != locator.is_checked():
            locator.check() if should_check else locator.uncheck()

    def select_radio_button(self, locator: Locator):
        """Selects a radio button."""
        locator.check()

    def upload_file(self, locator: Locator, file_path: str):
        """Uploads a file using the file input element."""
        locator.set_input_files(file_path)

    def download_file(self, page: Page, trigger: Locator, download_path: str):
        """Clicks the element that starts a download and saves the file to download_path."""
        with page.expect_download() as download_info:
            trigger.click()
        download_info.value.save_as(download_path)
        return download_path

    def intercept_request(self, context, url: str):
        """Intercepts network requests to the specified URL and allows for modification in the test method."""
        def handle_route(route: Route, request: Request):
            if url in request.url:
                response = route.fetch()
                original_data = response.json()

                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps(original_data)
                )
            else:
                route.continue_()

        context.route(url, handle_route)

    def explicit_wait(self, page: Page, locator: Locator, timeout: int):
        """Waits explicitly for a specific element to be visible with a customizable timeout."""
        locator.wait_for(state='visible', timeout=timeout)

    def scroll_down(self, page: Page, distance: int = 1000):
        """Scrolls down by the specified distance."""
        page.mouse.wheel(0, distance)

    def scroll_up(self, page: Page, distance: int = 1000):
        """Scrolls up by the specified distance."""
        page.mouse.wheel(0, -distance)
