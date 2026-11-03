# RPA & ARQUITETURA DE SOFTWARE

Iniciamos mais um projeto RPA, com Playwright. A ideia desse projeto não é criar uma grande automação complexa, mas atender demandas básicas de problemas do dia a dia, sem esquecer de temas importantes dentro do mundo da programação (POO, Arquitetura de Software, SOLID).

O foco desse projeto é o **(S) do SOLID - Single Responsibility Principle (Princípio da Responsabilidade Única)**.

Particularmente, gosto bastante desse tema, foi um dos conceitos que mais me ajudou a entender o que é um Clean Code, e principalmente, a identificar problemas no código, pontos de melhoria, apenas lembrando de algo: cada classe deve ter apenas uma responsabilidade.

Se uma classe fica complexa demais durante a construção do seu código, é um sinal para parar e entender qual é a responsabilidade principal que ela está assumindo, a partir daí, podemos separar as diferentes responsabilidades em outros componentes, deixando cada parte responsável por aquilo que realmente deveria resolver.

Esse projeto está sendo criado, como ambiente de estudos, para reforçar esse conhecimento, que julgo ser muito importante, se quisermos pensar em Clean Code.

RPA não pode ser desenvolvido de forma estática. Esses princípios precisam ser levados como pilares para o desenvolvimento como um todo.


___

## O que a automação faz

O robô acessa o site [Practice Test Automation](https://practicetestautomation.com/), entra na página **Test Table** e aplica os filtros:

1. Linguagem: `Python`
2. Nível: limpa `Beginner`, `Intermediate` e `Advanced`
3. Matrículas mínimas: `20+`
4. Ordenação: `Course Name`

Os valores ficam nas constantes do topo do `main.py`.

___

## Estrutura do projeto

```bash
main.py                      # Ponto de entrada e tratamento de erros
config/browser.py            # Configuração do navegador (modo Debug)
config/logging.py            # Configuração dos logs (console + JSON em logs/)
services/browser_service.py  # Abre e fecha Playwright, navegador e contexto
pages/base_page.py           # Classe base de todas as páginas
pages/initial_page.py        # Abre a página inicial
pages/patrice_page.py        # Acessa a página de desafios pelo menu
pages/test_table.py          # Acessa a página Test Table
pages/challenge_page.py      # Filtros da Test Table
utils/errors.py              # Exceções de negócio e técnicas
```

___

## Como executar

Requer Python 3.14+ e o [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run playwright install firefox
uv run python main.py
```

___

## Aplicação do **(S)**

Nesse projeto, vamos trabalhar o SRP dentro de todas as etapas do Browser, como configuração, serviço e a base para todo o projeto:

```bash
config/browser.py
services/browser_service.py
pages/base_page.py
```

Tive a ideia de implementar um modo de Debug no código. Ao invés de sair colocando `sleep()` por toda a extensão do código, criei uma configuração `config/browser.py`, onde consigo ligar e desligar o modo Debug, simplificando qualquer depuração da automação.

O modo Debug é controlado pela variável de ambiente `BROWSER_DEBUG`, lida do arquivo `.env`:

```bash
BROWSER_DEBUG=true
```

Incluí toda a configuração dentro desse módulo:

```python
@dataclass(frozen=True)
class BrowserConfig:
    """Parâmetros de inicialização do navegador."""

    debug: bool = os.getenv('BROWSER_DEBUG', 'False').lower() == 'true'

    @property
    def headless(self) -> bool:
        """Indica se o navegador deve rodar sem interface gráfica."""
        return not self.debug

    @property
    def slow_mo(self) -> int:
        """Atraso, em milissegundos, aplicado entre cada ação do Playwright."""
        return 500 if self.debug else 0
```

Se o Debug estiver como `True`, o navegador abre visível e com um atraso de 500ms entre as ações, onde conseguimos acompanhar e depurar a execução.

Vou implementar uma interação junto ao Log da aplicação, que quando o `Debug=True`, mude o nível dos logs, para um nível maior de detalhes.

___

## Tratamento de erros

Cada página só anota o contexto na exceção (`etapa`, `seletor`, valor usado) e relança. Quem registra o erro é o `main.py`, que converte cada tipo de falha em um código de saída para o orquestrador:

| Código | Situação |
|--------|----------|
| `0`  | Execução finalizada com sucesso |
| `10` | `BusinessError`: parâmetro inválido, ex.: valor de filtro que não existe no site. Reexecutar não resolve |
| `20` | `PlaywrightError` ou `TechnicalError`: timeout, elemento ausente ou desabilitado. Reexecutar pode resolver |
| `1`  | Erro inesperado (provável bug no robô) |

Antes de clicar em um filtro, o robô confere se o valor existe entre as opções. Assim, um valor errado nas constantes vira `BusinessError` com as opções disponíveis, em vez de esperar o timeout e aparecer como falha técnica.

___

## Padrão de código

- Código seguindo o **PEP 8**: imports agrupados (biblioteca padrão, externas, projeto), linhas de até 79 caracteres, 2 linhas em branco entre classes e funções de nível superior e 1 entre métodos.
- Docstrings seguindo o **PEP 257** no estilo Google (`Args`, `Returns`, `Raises`), em todos os módulos, classes e métodos.

Para conferir:

```bash
uvx ruff check --select E,W,F,I,D --ignore D203,D213,D413 --line-length 79 .
```

___

## Correções realizadas

- `filter_by_level_uncheck`: a condição estava invertida e o nível marcado nunca era desmarcado. Agora só retorna sem fazer nada quando o nível já está desmarcado.
- `filter_by_level_clear`: o log "Filtro limpo com sucesso" saía uma vez por nível; agora sai uma vez, após o loop.
- `filter_by_enrollments`: o log dizia "Level selecionado"; agora diz "Matrículas selecionadas com sucesso".
- As páginas passaram a importar `BasePage` de `pages/base_page.py`, onde ela é definida, em vez de `pages/initial_page.py`.
- Removidos imports sem uso (`datetime`, `UTC`) e o import de `sleep` saiu de dentro da função `main()` para o topo do arquivo.
