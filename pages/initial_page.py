from playwright.sync_api import Page

from pages.base_page import BasePage

import logging

logger = logging.getLogger(__name__)


class InitialPage(BasePage):

    '''
    Classe responsável por abrir a URL do projeto a ser altomattizado.

        É filha da classe BasePage, onde configuramos um padrão a ser abordado
        em todas as outras pages do projeto
    
    Args:
        page: Page - Objeto Playwright
        url: str - Url da página Web a ser automatizada
        timeout(opcional): int - Tempo padrão para esperar a execução ser
        finalizada
    '''

    def __init__(self, page: Page, url: str, timeout: int = 4_000) -> None:
        super().__init__(page, timeout)
        self.url = url


    def open_initial_page(self):

        '''
        Acessa a URL configurada para a página inicial, onde vamos partir

        Registra o log de inicio da navegação e informa que a página foi 
        carregada com sucesso. Caso ocorra allgum erro durante o acesso,
        levanta a exceção que é registrada

        Raise:
            Exception: Exceção gerada durante a navegação para a página.
        '''

        logger.info('Abrindo página inicial da automação ⏳')

        try:

            self.page.goto(self.url, timeout=self.timeout)
            logger.info('Sucesso ao abrir a página ✅')

        except Exception as e:
            
            logger.exception('Falha ao abrir o link ❌')
            logger.error('Error: ', e)
            raise