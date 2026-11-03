"""Exceções próprias do robô, usadas pelo main para definir a saída."""


class BusinessError(Exception):
    """Parâmetro ou regra de negócio impede o processamento.

    Ex.: valor de filtro que não existe no site. Reexecutar não resolve:
    alguém precisa corrigir.
    """


class TechnicalError(Exception):
    """Falha técnica detectada pelo próprio robô (ex.: elemento desabilitado).

    Recebe o mesmo tratamento das falhas do Playwright no main: reexecutar
    pode resolver.
    """
