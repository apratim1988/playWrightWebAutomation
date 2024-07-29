from playwright.sync_api import sync_playwright
import json


def test_run(playwright):
    browser = playwright.chromium.launch(headless=False,slow_mo=5000)
    context = browser.new_context()
    page = context.new_page()

    def handle_route(route, request):
        if "https://automationexercise.com/api/productsList" in request.url:
            response = route.fetch()
            original_data = response.json()

            for product in original_data["products"]:
                if product["id"] == 1:
                    product["name"] = "Mock Blue Top"

            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(original_data)
            )
        else:
            route.continue_()

    context.route("https://automationexercise.com/api/productsList", handle_route)
    page.goto("https://automationexercise.com/api/productsList")
    browser.close()


with sync_playwright() as playwright:
    test_run(playwright)
