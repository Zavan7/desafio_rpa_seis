"""Page Object da página inicial do site automatizado."""

import logging

from playwright.sync_api import Page

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class InitialPage(BasePage):
    """Classe responsável por abrir a URL do projeto a ser automatizado.

    É filha da classe BasePage, onde configuramos um padrão a ser abordado
    em todas as outras pages do projeto.

    Args:
        page(Page): Instância da página do Playwright.
        url(str): URL da página web a ser automatizada.
        timeout(int, opcional): Tempo máximo de espera, em milissegundos.
            Padrão 4.000ms.
    """

    def __init__(self, page: Page, url: str, timeout: int = 4_000) -> None:
        """Inicializa a página inicial.

        Args:
            page(Page): Instância da página do Playwright.
            url(str): URL da página inicial.
            timeout(int, opcional): Tempo máximo de espera. Padrão 4.000ms.
        """
        super().__init__(page, timeout)
        self.url = url

    def open_initial_page(self) -> None:
        """Acessa a URL da página inicial, de onde a automação parte.

        Registra o log de início da navegação e informa que a página foi
        carregada com sucesso. Caso ocorra algum erro durante o acesso,
        anota o contexto na exceção e a relança.

        Raises:
            Exception: Exceção gerada durante a navegação para a página.
        """
        logger.info('Abrindo página inicial da automação ⏳')

        try:
            self.page.goto(self.url, timeout=self.timeout)
            logger.info('Sucesso ao abrir a página ✅')

        except Exception as e:
            # Só anota o contexto e relança: quem registra o erro é o main.
            e.add_note(f'etapa: open_initial_page | url: {self.url}')
            raise
