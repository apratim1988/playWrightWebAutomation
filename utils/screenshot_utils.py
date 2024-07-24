import os
import time
from utils.config import Config

# Screenshot_utils (Under utils package under the root project directory)

import os
import time
from utils.config import Config

def capture_screenshot(page, test_case_name, step_name, data_set_id):
    # Create the base screenshot directory if it doesn't exist
    environment = os.getenv('ENVIRONMENT')
    if environment is None:
        raise ValueError("Environment variable 'ENVIRONMENT' is not set")
    screenshot_dir = os.path.join(Config.SCREENSHOT_DIR, environment, test_case_name)
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    # Create subdirectory for the data set
    data_set_dir = os.path.join(screenshot_dir, f"data_set_{data_set_id}")
    if not os.path.exists(data_set_dir):
        os.makedirs(data_set_dir)

    # Add a timestamp to the screenshot filename to make it unique
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_path = os.path.join(data_set_dir, f"{step_name}_{timestamp}.png")

    # Capture and save the screenshot
    page.screenshot(path=screenshot_path)
