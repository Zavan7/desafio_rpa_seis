from playwright.sync_api import sync_playwright
from datetime import UTC, datetime

from pages.initial_page import InitialPage
from pages.patrice_page import PatricePage
from pages.test_table import TestTable

from config.browser import BrowserConfig
from config.logging import setup_logging
import logging

URL = 'https://practicetestautomation.com/'
LOCATOR_PATRICE = '#menu-item-20'
LOCATOR_TEST_TABLE = "//a[text()='Test Table']"

logger = logging.getLogger(__name__)

def main() -> None:

    setup_logging()

    config = BrowserConfig()

    try:

        with sync_playwright() as p:
            browser = p.firefox.launch(
                headless= config.headless,
                slow_mo=config.slow_mo,
            )
            page = browser.new_page()


            initial_page = InitialPage(page, URL)
            initial_page.open_initial_page()

            patrice_page = PatricePage(page, LOCATOR_PATRICE)
            patrice_page.click_patrice()

            test_table = TestTable(page, LOCATOR_TEST_TABLE)
            test_table.test_table()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()