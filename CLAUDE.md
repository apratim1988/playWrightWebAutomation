# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Python + pytest + Playwright (sync API) UI automation framework targeting saucedemo.com, using the Page Object Model, Excel-driven test data, and per-environment configuration.

## Setup & commands

`requirements.txt` is **UTF-16 LE** encoded (pip handles it; grep/sed need `iconv -f utf-16` first).

```bash
pip install -r requirements.txt
playwright install

# Run the suite (run from repo root so `pages`, `tests`, `utils` import as packages)
pytest tests -v -s --environment=production --playwright-browser=chromium

# Single test
pytest tests/test_place_order.py::TestPlaceOrder::test_place_order -v -s --environment=qa

# Visual regression tests (pytest-playwright-visual); refresh baselines with --update-snapshots
pytest visual_tests -v --update-snapshots
```

- Custom options are defined in `tests/conftest.py` (duplicated verbatim in `visual_tests/conftest.py` — keep both in sync):
  - `--environment` = `production` (default) | `beta` | `dev` | `qa` → URL from `utils/environment_urls.py`
  - `--playwright-browser` = `chromium` (default) | `firefox` | `webkit`. This is deliberately not `--browser`, which belongs to the installed pytest-playwright plugin. Browsers always launch headless.
- `pytest.ini` always writes an HTML report to `report/report.html` (pytest-html, self-contained).
- CI: `Jenkinsfile` only seeds jobs via Job DSL; `jenkins/job_dsl.groovy` creates one job per environment that runs all three browsers, pulling `<env>-username`/`<env>-password` Jenkins credentials.

## Architecture

**Test flow.** Tests are classes that subclass `tests/base_test.py::BaseTest` and take the `set_up_tear_down` fixture (a fresh context + page at 1536x800, already navigated to the environment URL) plus a `data` param. Each test calls `self.initialize_logger(data['id'])` first, wraps its steps in try/except, and routes failures through `self.fail_test(...)`, which logs, takes a screenshot, and calls `pytest.fail`. New tests should follow `tests/test_place_order.py`.

**Data-driven parametrization.** `pytest_generate_tests` in conftest parametrizes any test that requests a `data` fixture:
- Workbook: `testData/test_data.xlsx` for production, `testData/test_data_<env>.xlsx` otherwise (`Config.get_excel_file_path`). Only production and beta workbooks exist, so `dev`/`qa` runs will fail until those are added.
- Sheet name = the test function name lowercased. A new data-driven test needs a matching sheet in every environment's workbook.
- Each row becomes a dict keyed by the header row. It needs an `id` column (used for log and screenshot folders) and, for order tests, `product`. `utils/excel_utils.py` adds Faker-generated `first_name`, `last_name` and `zipcode` to every row.

**Environment state through `os.environ`.** The `environment` fixture sets `ENVIRONMENT`, and `BaseTest.read_credentials`, `utils/logger_utils.py` and `utils/screenshot_utils.py` all read it. Credentials come from the `TEST_USERNAME`/`TEST_PASSWORD` env vars (set by Jenkins) if both are set, otherwise from the git-ignored `utils/credentials.json`, keyed by environment name with `username`/`password` entries. Never log the password.

**Artifacts.** Logs go to `logs/<env>/<test_name>/data_set_<id>/` and screenshots to `screenshot/<env>/<test_name>/data_set_<id>/`. `BaseTest.setup_method` clears both folders for each test method the first time that method runs (tracked per class in `_cleared_methods`).

**Page objects** (`pages/`) take `(page, logger)`, and navigation methods return the next page object: `LoginPage.do_login(credentials, product)` returns `ProductListPage`, then `click_cart_icon()` returns `CartPage`, then `click_checkout_button()` returns `CheckoutPage`. `ProductListPage` builds its add-to-cart locator from the product name in its constructor.

**Self-healing locators.** `LoginPage` defines each element as an ordered list of `(strategy, value)` tuples. `utils/element_utils.find_element_with_fallback` returns the first one that is visible and logs a warning when it falls back. Supported strategies: `placeholder`, `id`, `class`, `text`, `css`, `xpath`, `data-test`. `data-test` builds `[data-test="..."]`. The helper checks visibility once without waiting, so elements that appear after an action (error messages, the login button after logout) are exposed as plain locators for `expect()`. The other page objects use plain `page.locator` XPaths.

## Known quirks

- `tests/test_login.py`, `test_logout.py` and `test_add_to_cart.py` are not data-driven (no `data` param, no Excel sheet); their artifacts go under `data_set_1`.
- `set_up_tear_down` sets `self.page` on the test instance; the `pytest_runtest_makereport` hook in conftest embeds the failure screenshot (the one `fail_test` took) into the HTML report as base64.
- `mock/test_mockapi.py` runs a headed browser at import time (it has a module-level `sync_playwright()` block). It is a standalone route-interception demo, not part of the suite.
- `utils/mongo_utils.py` (needs the `MONGO_URI` env var) and `utils/network_status_utils.py` are helpers that no test uses yet.
- `.github/mcp.json` configures a local Playwright MCP server.
