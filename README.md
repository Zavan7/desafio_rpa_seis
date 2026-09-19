# RPA & ARQUITETURA DE SOFTWARE

Iniciamos mais um projeto RPA, com Playwright. A ideia desse projeto não é criar uma grande automação complexa, mas atender demandas básicas de problemas do dia a dia, sem esquecer de temas importantes dentro do mundo da programação (POO, Arquitetura de Software, SOLID).

O foco desse projeto é focar no **(S)do SOLID - Single Responsibility Principle (Princípio da Responsabilidade Única)**.

Particularmente, gosto bastante desse tema, foi um dos conceitos que mais me ajudou a entender o que é um Clean Code, e principalmente, a identificar problemas no código, pontos de melhoria, apenas lembrando de algo: cada classe deve ter apenas uma responsabilidade.

Se uma classe fica complexa demais durante a construção do seu código, é um sinal para parar e entender qual é a responsabilidade principal que ela está assumindo, a partir daí, podemos separar as diferentes responsabilidades em outros componentes, deixando cada parte responsável por aquilo que realmente deveria resolver.

Esse projeto está sendo criado, como ambiente de estudos, para reforçar esse conhecimento, que julgo ser muito importante, se quisermos pensar em CleanCode

RPA não pode ser desenvolvido de forma estática. Esses princípios precisam ser levados como pilares para o desenvolvimento como um todo.


___

## Aplicação do **(S)**

Nesse projeto, vamos trabalhar o SRP, dentro de todas as etapas do Browser, como configuração, serviço e a base para todo o projeto

```bash
config/browser.py
services/browser_service.py
pages/initial_page.py
```

Tive a ideia de implementar um modo de Debug no código, ao invés de sair colocando `sleep()`, por toda a extenção do código, criei uma configuração `config/browser.py`, onde consegue ligar e desligar o modo Debug do código, simplificando qualquer depuração da automação.

Inclui toda a configuração dentro desse módulo:

```python
from dataclasses import dataclass



@dataclass(frozen=True)
class BrowserConfig:
    debug: bool = False

    
    @property
    def headless(self) -> bool:
        return not self.debug


    @property
    def slow_mo(self) -> int:
        return 500 if self.debug else 0

```

Se o Debug estiver como `True`, ele libera algumas permições, onde conseguimos debugar.

Vou implementar uma interação junto ao Log da aplicação, que quando o `Debug=True`, mude o nível dos logs, para um nível maior de detalhes