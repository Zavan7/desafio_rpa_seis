"""Configuração do navegador usado pela automação.

Lê a variável de ambiente BROWSER_DEBUG (via .env) para decidir se o
navegador abre visível e em câmera lenta, útil para depuração.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class BrowserConfig:
    """Parâmetros de inicialização do navegador.

    Attributes:
        debug(bool): True quando BROWSER_DEBUG=true. Em modo debug o
            navegador abre visível e com atraso entre as ações.
    """

    debug: bool = os.getenv('BROWSER_DEBUG', 'False').lower() == 'true'

    @property
    def headless(self) -> bool:
        """Indica se o navegador deve rodar sem interface gráfica.

        Returns:
            bool: False em modo debug, True caso contrário.
        """
        return not self.debug

    @property
    def slow_mo(self) -> int:
        """Atraso, em milissegundos, aplicado entre cada ação do Playwright.

        Returns:
            int: 500 em modo debug, 0 caso contrário.
        """
        return 500 if self.debug else 0
