import logging

from playwright.sync_api import Page

from pages.initial_page import BasePage


logger = logging.getLogger(__name__)

class PatricePage(BasePage):
    def __init__(self, page: Page, locator_patrice: str, timeout: int = 4_000):
        super().__init__(page, timeout)
        self.locator_patrice = locator_patrice


    def click_patrice(self) -> None:


        logger.info('Direcionando a página de desafios ⏳')
        try:
            self.page.wait_for_selector(
                self.locator_patrice,
                timeout=self.timeout
            )

            self.page.locator(self.locator_patrice).click()

            logger.info('Página de desafios localizada ✅')

        except Exception as e:
            logger.error(
                f'Error: {e}, não foi possível atender a solicitação ❌'
            )