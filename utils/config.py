import os


class Config:

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    def get_excel_file_path(env):
        file_name = f'test_data_{env}.xlsx' if env != 'production' else 'test_data.xlsx'
        return os.path.join(Config.BASE_DIR, 'testData', file_name)

    @staticmethod
    def get_sheet_name(test_case_name):
        return test_case_name.lower()