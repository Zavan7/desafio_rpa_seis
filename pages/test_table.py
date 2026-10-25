import logging

from playwright.sync_api import Page

from pages.initial_page import BasePage


logger = logging.getLogger(__name__)

class TestTable(BasePage):
    def __init__(
        self,
        page: Page,
        locator_test_table: str,
        timeout: int = 4_000
    ):
        super().__init__(page, timeout)
        self.locator_test_table = locator_test_table


    def test_table(self) -> None:


        logger.info('Direcionando a página de Test Table ⏳')
        try:
            self.page.wait_for_selector(
                self.locator_test_table,
                timeout=self.timeout
            )

            self.page.locator(self.locator_test_table).click()

            # self.page.locator(self.locator_test_table).nth()

            logger.info('Página Test Table localizada ✅')

        except Exception as e:
            logger.error(
                f'Error: {e}, não foi possível atender a solicitação ❌'
            )