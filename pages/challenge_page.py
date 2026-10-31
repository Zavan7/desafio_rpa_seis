import logging

from playwright.sync_api import Page

from pages.initial_page import BasePage

logger = logging.getLogger(__name__)


class AssortedFilters(BasePage):
    '''
    Classe responsável pelos vários filtros ao longo da aplicação

    Filtros de Linguagem (filter_by_language),
        Nível de dificuldade do curso(filter_by_level check | uncheck | clear),
        Matrículas mínimas(filter_by_enrollments),
        Ordenação da lista de cursos(sort_by)

        
    '''
    def __init__ (
        self,
        page: Page,
        filter_seletor: str,
        timeout: int =4_000
    ) -> None:

        super().__init__(page, timeout)
        self.filter_seletor = filter_seletor


    def filter_by_language(self, language: str) -> None:
        try:
            language_filter =  self.page.locator(
                self.filter_seletor
            ).get_by_label(language)

            if language_filter.is_checked(timeout=self.timeout):
                logger.info('Linguagem já selecionada ✅')
                return
            
            language_filter.check(timeout=self.timeout)
            logger.info('Feito a seleção da linguagem ✅')

        except Exception as e:
            print(f'Error: {e} ❌')
            raise


    def filter_by_level_uncheck(self, level: str) -> None:
        try:
            filter_by_level_checked = self.page.locator(
                self.filter_seletor
            ).get_by_label(level)


            if filter_by_level_checked.is_checked():
                logger.info('Removendo filtro ⏳')
                return
            
            filter_by_level_checked.uncheck()

        except:
            ...
    

    def filter_by_level_check(self, level: str) -> None:
        try:
            filter_by_level_checked = self.page.locator(
                self.filter_seletor
            ).get_by_label(level)


            if filter_by_level_checked.is_checked():
                logger.info('Level já selecionado ✅')
                return
            
            filter_by_level_checked.check()

        except:
            ...


    def filter_by_level_clear(self, levels: list[str]) -> None:
        try:
            filter_by_level_clear = self.page.locator(
                self.filter_seletor
            )

            for level in levels:
                filter_by_level_clear.get_by_label(level).uncheck()     

        except:
            ...


    def filter_by_enrollments(self, enrollments: str) -> None:
        ...

    
    def sort_by(self, value: str) -> None:
        ...