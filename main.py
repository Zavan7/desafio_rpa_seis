"""Ponto de entrada do robô de automação do site Practice Test Automation.

Abre o site, navega até a página Test Table e aplica os filtros de
linguagem, nível, matrículas e ordenação definidos nas constantes abaixo.

Códigos de saída (lidos pelo orquestrador):
    0: Execução finalizada com sucesso.
    1: Erro inesperado (provável bug no robô).
    10: Execução interrompida por regra de negócio.
    20: Falha técnica (timeout, elemento ausente, site fora do ar).
"""

import logging
from time import sleep

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from config.browser import BrowserConfig
from config.logging import setup_logging
from pages.challenge_page import AssortedFilters
from pages.initial_page import InitialPage
from pages.patrice_page import PatricePage
from pages.test_table import TestTable
from utils.errors import BusinessError, TechnicalError

URL = 'https://practicetestautomation.com/'
LOCATOR_PATRICE = '#menu-item-20'
LOCATOR_TEST_TABLE = "//a[text()='Test Table']"
FILTER_SELETOR_LANGUAGE = 'fieldset.filter-group:nth-child(1)'
FILTER_SELETOR_LEVEL = 'fieldset.filter-group:nth-child(2)'
FILTER_SELETOR_ENROLLMENTS = 'fieldset.filter-group:nth-child(3)'
FILTER_SELETOR_ORDER_BY = '#sortBy'
LANGUAGE = 'Python'
LEVEL_LIST = ['Beginner', 'Intermediate', 'Advanced']
ENROLLMENTS_VALUE = '20+'
ORDER_BY_VALUE = 'Course Name'


logger = logging.getLogger(__name__)


def main() -> None:
    """Executa o fluxo completo da automação.

    Configura o logging, abre o Firefox conforme o BrowserConfig e percorre
    as páginas aplicando os filtros. Cada tipo de falha é convertido em um
    código de saída para que o orquestrador saiba o status da execução.

    Raises:
        SystemExit: Com código 10 para BusinessError, 20 para falhas
            técnicas (PlaywrightError ou TechnicalError) e 1 para qualquer
            outro erro.
    """
    setup_logging()

    try:
        config = BrowserConfig()

        with sync_playwright() as p:
            browser = p.firefox.launch(
                headless=config.headless,
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

            assorted_filters_enrollments = AssortedFilters(
                page,
                FILTER_SELETOR_ENROLLMENTS
            )
            assorted_filters_enrollments.filter_by_enrollments(
                ENROLLMENTS_VALUE
            )

            assorted_filter_order_by = AssortedFilters(
                page,
                FILTER_SELETOR_ORDER_BY
            )
            assorted_filter_order_by.sort_by(ORDER_BY_VALUE)

            sleep(3)

        logger.info('Execução finalizada com sucesso ✅')

    # O Maestro decide o status pelo código de saída: sem isto, a
    # falha sairia com 0 e seria marcada como sucesso.
    except BusinessError as e:
        # Parâmetro inválido: sem traceback, o problema não é o código.
        logger.warning(
            'Execução interrompida por regra de negócio: %s | %s',
            e,
            ' | '.join(getattr(e, '__notes__', [])),
        )
        raise SystemExit(10) from e

    except (PlaywrightError, TechnicalError) as e:
        # Timeout, elemento ausente, site fora do ar: reexecutar pode resolver.
        logger.exception('Falha técnica na execução')
        raise SystemExit(20) from e

    except Exception as e:
        # Qualquer outra coisa é bug no robô.
        logger.critical('Erro inesperado (provável bug)', exc_info=True)
        raise SystemExit(1) from e


if __name__ == '__main__':
    main()
