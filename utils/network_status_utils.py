
import logging
from playwright.sync_api import Page, Response

class NetworkUtils:
    def __init__(self):
        self.logger = logging.getLogger('NetworkUtils')

    def log_request(self, response: Response):
        self.logger.info(f"Request to {response.url} returned status code {response.status}")
        return response.status

    def capture_network_status(self, page: Page, operation_callback):
        """Performs the operation and logs network status codes"""
        try:
            def log_request_handler(response: Response):
                self.log_request(response)

            page.on("response", log_request_handler)
            operation_callback(page)
        except Exception as e:
            self.logger.error(f"Error during network inspection: {e}")
            raise
