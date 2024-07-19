import pytest
import os
import json
import shutil
from utils.config import Config
from utils.logger_utils import setup_logger
from utils.screenshot_utils import capture_screenshot

@pytest.mark.usefixtures("set_up_tear_down")
class BaseTest:
    @classmethod
    def setup_class(cls):
        Config.ensure_directories()

    @classmethod
    def clear_screenshot_for_method(cls, method_name):
        screenshot_dir = os.path.join(Config.SCREENSHOT_DIR, method_name)
        if os.path.exists(screenshot_dir):
            shutil.rmtree(screenshot_dir)

    def setup_method(self, method):
        Config.ensure_directories()
        self.method_name = method.__name__

        # Only clear the screenshots directory once per method
        if not hasattr(self, 'method_setup_done'):
            self.clear_screenshot_for_method(self.method_name)
            self.__class__.method_setup_done = True

    def initialize_logger(self, data_set_id):
        self.data_set_id = data_set_id
        self.logger = setup_logger(self.method_name, self.data_set_id)

    def take_screenshot(self, page, step_name, data_set_id):
        # Delegate to the util function, using method info
        capture_screenshot(page, self.method_name, step_name, data_set_id)

    def fail_test(self, page, error_message, data_set_id):
        self.logger.error(error_message, exc_info=True)
        self.take_screenshot(page, 'error', data_set_id)
        pytest.fail(error_message, pytrace=False)

    @staticmethod
    def read_credentials():
        with open(Config.CREDENTIALS_FILE_PATH, 'r') as file:
            credentials = json.load(file)
        return credentials