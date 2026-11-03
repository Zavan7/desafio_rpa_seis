"""Serviço que controla o ciclo de vida do navegador Playwright."""

import logging

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

from config.browser import BrowserConfig

logger = logging.getLogger(__name__)


class BrowserService:
    """Abre e fecha o Playwright, o navegador e o contexto de navegação.

    Args:
        config(BrowserConfig): Configuração de headless e slow_mo usada
            ao iniciar o navegador.
    """

    def __init__(self, config: BrowserConfig):
        """Inicializa o serviço sem abrir nenhum recurso.

        Args:
            config(BrowserConfig): Configuração do navegador.
        """
        self.config = config
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None

    def start(self) -> Page:
        """Inicia o Playwright, abre o Firefox e cria uma nova página.

        Se qualquer etapa falhar, fecha o que já foi aberto antes de
        relançar o erro, evitando processos do navegador órfãos.

        Returns:
            Page: Página pronta para navegação.

        Raises:
            Exception: Erro ocorrido ao abrir o navegador ou o contexto.
        """
        self.playwright = sync_playwright().start()

        try:
            self.browser = self.playwright.firefox.launch(
                headless=self.config.headless,
                slow_mo=self.config.slow_mo
            )

            self.context = self.browser.new_context()

            return self.context.new_page()

        except Exception:
            # Libera o que já foi aberto e deixa o erro subir.
            self.close()
            raise

    def close(self) -> None:
        """Fecha o contexto, o navegador e encerra o Playwright.

        Falhas ao fechar um recurso são apenas registradas como warning,
        para que os demais recursos também sejam fechados.
        """
        # Cada recurso fecha mesmo que o anterior falhe ao fechar.
        for name in ('context', 'browser'):
            resource = getattr(self, name)

            if resource:
                try:
                    resource.close()
                except Exception:
                    logger.warning(
                        'Falha ao fechar recurso do navegador',
                        extra={'dados': {'recurso': name}},
                        exc_info=True,
                    )

        if self.playwright:
            self.playwright.stop()
