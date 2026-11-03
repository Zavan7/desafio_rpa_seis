"""Page Object dos filtros da página Test Table."""

import logging

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.errors import BusinessError, TechnicalError

logger = logging.getLogger(__name__)


class AssortedFilters(BasePage):
    """Classe responsável pelos vários filtros ao longo da aplicação.

    Cada instância atua sobre um grupo de filtro, identificado pelo seletor
    recebido no construtor:
        Linguagem: filter_by_language.
        Nível de dificuldade do curso: filter_by_level_check,
            filter_by_level_uncheck e filter_by_level_clear.
        Matrículas mínimas: filter_by_enrollments.
        Ordenação da lista de cursos: sort_by.

    Args:
        page(Page): Instância da página do Playwright.
        filter_seletor(str): Seletor do grupo de filtro a ser manipulado.
        timeout(int, opcional): Tempo máximo de espera, em milissegundos.
            Padrão 4.000ms.
    """

    def __init__(
        self,
        page: Page,
        filter_seletor: str,
        timeout: int = 4_000
    ) -> None:
        """Inicializa o filtro.

        Args:
            page(Page): Instância da página do Playwright.
            filter_seletor(str): Seletor do grupo de filtro.
            timeout(int, opcional): Tempo máximo de espera. Padrão 4.000ms.
        """
        super().__init__(page, timeout)
        self.filter_seletor = filter_seletor

    def _ensure_option(self, value: str, option_seletor: str) -> None:
        """Confere se o valor pedido existe entre as opções do filtro.

        Sem isto, um valor errado nas constantes faz o Playwright ficar
        procurando o elemento até estourar o timeout, e a falha aparece como
        técnica quando o problema é o parâmetro.

        Args:
            value(str): Texto da opção que deve existir no filtro.
            option_seletor(str): Seletor das opções dentro do grupo
                (ex.: 'label', 'option', '[role="option"]').

        Raises:
            BusinessError: O valor não existe no filtro. A mensagem traz as
                opções disponíveis.
        """
        group = self.page.locator(self.filter_seletor)
        group.wait_for(timeout=self.timeout)

        options = [
            option.strip()
            for option in group.locator(option_seletor).all_text_contents()
        ]

        if value not in options:
            raise BusinessError(
                f"Valor '{value}' não existe no filtro. Opções: {options}"
            )

    def filter_by_language(self, language: str) -> None:
        """Marca a linguagem informada no filtro de linguagens.

        Se a linguagem já estiver marcada, apenas registra o log e retorna.

        Args:
            language(str): Rótulo da linguagem (ex.: 'Python').

        Raises:
            BusinessError: A linguagem não existe no filtro.
            Exception: Falha do Playwright ao localizar ou marcar a opção.
        """
        try:
            self._ensure_option(language, 'label')

            language_filter = self.page.locator(
                self.filter_seletor
            ).get_by_label(language)

            if language_filter.is_checked(timeout=self.timeout):
                logger.info('Linguagem já selecionada ✅')
                return

            language_filter.check(timeout=self.timeout)
            logger.info('Feito a seleção da linguagem ✅')

        except Exception as e:
            # Só anota o contexto e relança: quem registra o erro é o main.
            e.add_note(
                f'etapa: filter_by_language | seletor: {self.filter_seletor}'
                f' | linguagem: {language}'
            )
            raise

    def filter_by_level_uncheck(self, level: str) -> None:
        """Desmarca o nível de dificuldade informado.

        Args:
            level(str): Rótulo do nível (ex.: 'Beginner').

        Raises:
            BusinessError: O nível não existe no filtro.
            Exception: Falha do Playwright ao localizar ou desmarcar a opção.
        """
        try:
            self._ensure_option(level, 'label')

            filter_by_level_checked = self.page.locator(
                self.filter_seletor
            ).get_by_label(level)

            if not filter_by_level_checked.is_checked(timeout=self.timeout):
                logger.info('Level já desmarcado ✅')
                return

            logger.info('Removendo filtro ⏳')
            filter_by_level_checked.uncheck(timeout=self.timeout)

        except Exception as e:
            e.add_note(
                f'etapa: filter_by_level_uncheck'
                f' | seletor: {self.filter_seletor}'
                f' | level: {level}'
            )
            raise

    def filter_by_level_check(self, level: str) -> None:
        """Marca o nível de dificuldade informado.

        Se o nível já estiver marcado, apenas registra o log e retorna.

        Args:
            level(str): Rótulo do nível (ex.: 'Intermediate').

        Raises:
            BusinessError: O nível não existe no filtro.
            Exception: Falha do Playwright ao localizar ou marcar a opção.
        """
        try:
            self._ensure_option(level, 'label')

            filter_by_level_checked = self.page.locator(
                self.filter_seletor
            ).get_by_label(level)

            if filter_by_level_checked.is_checked(timeout=self.timeout):
                logger.info('Level já selecionado ✅')
                return

            filter_by_level_checked.check(timeout=self.timeout)

        except Exception as e:
            e.add_note(
                f'etapa: filter_by_level_check'
                f' | seletor: {self.filter_seletor}'
                f' | level: {level}'
            )
            raise

    def filter_by_level_clear(self, levels: list[str]) -> None:
        """Desmarca todos os níveis de dificuldade informados.

        Valida todos os níveis antes de desmarcar qualquer um, para não
        deixar o filtro pela metade caso algum valor seja inválido.

        Args:
            levels(list[str]): Rótulos dos níveis a desmarcar.

        Raises:
            BusinessError: Algum dos níveis não existe no filtro.
            Exception: Falha do Playwright ao localizar ou desmarcar as
                opções.
        """
        try:
            filter_by_level_clear = self.page.locator(
                self.filter_seletor
            )

            # Valida todos antes de mexer em qualquer um.
            for level in levels:
                self._ensure_option(level, 'label')

            for level in levels:
                filter_by_level_clear.get_by_label(level).uncheck(
                    timeout=self.timeout
                )

            logger.info('Filtro limpo com sucesso ✅')

        except Exception as e:
            e.add_note(
                f'etapa: filter_by_level_clear'
                f' | seletor: {self.filter_seletor}'
                f' | levels: {levels}'
            )
            raise

    def filter_by_enrollments(self, enrollments: str) -> None:
        """Seleciona a quantidade mínima de matrículas no dropdown.

        Args:
            enrollments(str): Texto exato da opção (ex.: '20+').

        Raises:
            BusinessError: A opção não existe no dropdown.
            Exception: Falha do Playwright ao abrir o dropdown ou clicar na
                opção.
        """
        try:
            # As opções já estão no HTML, mesmo com o dropdown fechado.
            self._ensure_option(enrollments, '[role="option"]')

            filter_dropdown = self.page.locator(
                self.filter_seletor
            )

            filter_dropdown.click(timeout=self.timeout)

            filter_dropdown.get_by_text(
                enrollments,
                exact=True
            ).click(timeout=self.timeout)

            logger.info('Matrículas selecionadas com sucesso ✅')

        except Exception as e:
            e.add_note(
                f'etapa: filter_by_enrollments'
                f' | seletor: {self.filter_seletor}'
                f' | matriculas: {enrollments}'
            )
            raise

    def sort_by(self, value: str) -> None:
        """Ordena a lista de cursos pela opção informada no select.

        Args:
            value(str): Rótulo da opção de ordenação (ex.: 'Course Name').

        Raises:
            BusinessError: A opção não existe no select.
            TechnicalError: O select de ordenação está desabilitado.
            Exception: Falha do Playwright ao selecionar a opção.
        """
        try:
            sorted_by = self.page.locator(
                self.filter_seletor
            )

            self._ensure_option(value, 'option')

            if sorted_by.is_enabled(timeout=self.timeout):
                sorted_by.select_option(label=value, timeout=self.timeout)

                logger.info('Lista ordenada com sucesso ✅')

            else:
                # Sem isto, o robô terminava com sucesso sem ordenar.
                raise TechnicalError('Select de ordenação desabilitado')

        except Exception as e:
            e.add_note(
                f'etapa: sort_by | seletor: {self.filter_seletor}'
                f' | ordenacao: {value}'
            )
            raise
