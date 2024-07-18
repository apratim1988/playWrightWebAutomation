import os
import time
from utils.config import Config

def capture_screenshot(page, test_case_name, step_name, data_set_id):
    screenshot_dir = os.path.join(Config.SCREENSHOT_DIR, test_case_name)
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    data_set_dir = os.path.join(screenshot_dir, f"data_set_{data_set_id}")
    if not os.path.exists(data_set_dir):
        os.makedirs(data_set_dir)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_path = os.path.join(data_set_dir, f"{step_name}_{timestamp}.png")
    page.screenshot(path=screenshot_path)

    return screenshot_path  # Return the path where the screenshot is saved
