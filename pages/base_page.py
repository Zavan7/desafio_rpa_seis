from playwright.sync_api import Page


class BasePage():

    '''
    Classe base para todas as páginas da automação
    
    Armazena a instância da página do Playwright e o tempo padrão
    de espera utilizados palas classes filhas
    '''

    def __init__(self, page: Page, timeout: int = 4_000):
        '''
        Inicializa a classe base

        Args:
            page(Page): Instância da página do Playwright
            timeout(int, opicional): Tempo máximo de espera para operações
                na página. Padrão 4.000ms.

                Esse timeout é isolado junto a página, pois pode ser ajustado
                dependendo do projeto, caso haja nescecidade de aumentar, ou
                diminuir para otimizar o tempo da automação
        '''

        self.page = page
        self.timeout = timeout