import os


class Config:
    # Define base directories
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Define paths for various directories and files
    EXCEL_FILE_PATH = os.path.join(BASE_DIR, 'testData', 'test_data.xlsx')
    CREDENTIALS_FILE_PATH = os.path.join(BASE_DIR, 'utils', 'credentials.json')
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    SCREENSHOT_DIR = os.path.join(BASE_DIR, 'screenshot')

    # REPORT_DIR = os.path.join(BASE_DIR, 'report')

    @staticmethod
    def ensure_directories():
        # Ensure that necessary directories exist
        dirs = [Config.LOG_DIR, Config.SCREENSHOT_DIR]
        for directory in dirs:
            if not os.path.exists(directory):
                os.makedirs(directory)

    @staticmethod
    def get_sheet_name(test_case_name):
        # Example logic to determine the sheet name based on the test case name
        return f'test_{test_case_name.lower()}'
