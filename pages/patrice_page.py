"""Page Object do menu que leva à página de desafios (Practice)."""

import logging

from playwright.sync_api import Page

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class PatricePage(BasePage):
    """Classe responsável por acessar a página de desafios a partir do menu.

    Args:
        page(Page): Instância da página do Playwright.
        locator_patrice(str): Seletor do item de menu da página de desafios.
        timeout(int, opcional): Tempo máximo de espera, em milissegundos.
            Padrão 4.000ms.
    """

    def __init__(self, page: Page, locator_patrice: str, timeout: int = 4_000):
        """Inicializa a página de desafios.

        Args:
            page(Page): Instância da página do Playwright.
            locator_patrice(str): Seletor do item de menu.
            timeout(int, opcional): Tempo máximo de espera. Padrão 4.000ms.
        """
        super().__init__(page, timeout)
        self.locator_patrice = locator_patrice

    def click_patrice(self) -> None:
        """Aguarda o item de menu aparecer e clica nele.

        Raises:
            Exception: Elemento não encontrado no tempo limite ou falha no
                clique. A exceção recebe uma nota com a etapa e o seletor.
        """
        logger.info('Direcionando a página de desafios ⏳')
        try:
            self.page.wait_for_selector(
                self.locator_patrice,
                timeout=self.timeout
            )

            self.page.locator(self.locator_patrice).click()

            logger.info('Página de desafios localizada ✅')

        except Exception as e:
            # Só anota o contexto e relança: quem registra o erro é o main.
            e.add_note(
                f'etapa: click_patrice | seletor: {self.locator_patrice}'
            )
            raise
