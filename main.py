from playwright.sync_api import sync_playwright
from datetime import UTC, datetime

from pages.initial_page import InitialPage
from pages.patrice_page import PatricePage
from pages.test_table import TestTable
from pages.challenge_page import AssortedFilters

from config.browser import BrowserConfig
from config.logging import setup_logging
import logging

URL = 'https://practicetestautomation.com/'
LOCATOR_PATRICE = '#menu-item-20'
LOCATOR_TEST_TABLE = "//a[text()='Test Table']"
FILTER_SELETOR_LANGUAGE = 'fieldset.filter-group:nth-child(1)'
FILTER_SELETOR_LEVEL = 'fieldset.filter-group:nth-child(2)'
LANGUAGE = 'Python'
LEVEL_LIST = ['Beginner', 'Intermediate', 'Advanced']


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

            assorted_filters_language = AssortedFilters(
                page,
                FILTER_SELETOR_LANGUAGE
            )
            assorted_filters_language.filter_by_language(LANGUAGE)


            assorted_filters_level = AssortedFilters(
                page,
                FILTER_SELETOR_LEVEL
            )
            assorted_filters_level.filter_by_level_clear(LEVEL_LIST)

            from time import sleep
            sleep(3)

    except Exception as e:
        print(e)
        # O Maestro decide o status pelo código de saída: sem isto, a
        # falha sairia com 0 e seria marcada como sucesso.
        raise SystemExit(1) from e


if __name__ == '__main__':
    main()