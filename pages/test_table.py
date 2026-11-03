"""Page Object do link que leva à página Test Table."""

import logging

from playwright.sync_api import Page

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class TestTable(BasePage):
    """Classe responsável por acessar a página Test Table.

    Args:
        page(Page): Instância da página do Playwright.
        locator_test_table(str): Seletor do link da página Test Table.
        timeout(int, opcional): Tempo máximo de espera, em milissegundos.
            Padrão 4.000ms.
    """

    def __init__(
        self,
        page: Page,
        locator_test_table: str,
        timeout: int = 4_000
    ):
        """Inicializa a página Test Table.

        Args:
            page(Page): Instância da página do Playwright.
            locator_test_table(str): Seletor do link da página.
            timeout(int, opcional): Tempo máximo de espera. Padrão 4.000ms.
        """
        super().__init__(page, timeout)
        self.locator_test_table = locator_test_table

    def test_table(self) -> None:
        """Aguarda o link da Test Table aparecer e clica nele.

        Raises:
            Exception: Elemento não encontrado no tempo limite ou falha no
                clique. A exceção recebe uma nota com a etapa e o seletor.
        """
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
            # Só anota o contexto e relança: quem registra o erro é o main.
            e.add_note(
                f'etapa: test_table | seletor: {self.locator_test_table}'
            )
            raise
