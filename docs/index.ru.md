<h1 align="center">Добро пожаловать в Python-Multibar!</h1>

<img src="https://media.giphy.com/media/UeRFyF2fJcfnwjVkIn/giphy.gif" align="left" width="200px"/>

Проект: python-multibar
<br>
Лицензия: Apache 2.0
<br>
Описание: Tool for static progress bars writing.
<br>
ОС: Независим
<br>
Python: 3.9+
<br>
Typing: Typed
<br>
Тема: Утилиты
<br />
    <p align="center">
    <br />
    <a href="https://pypi.org/project/python-multibar/">Мы на PyPi</a>
    ·
    <a href="https://github.com/Animatea/python-multibar/issues">Сообщить о баге</a>
    ·
    <a href="https://github.com/Animatea/python-multibar/issues">Предложить идею</a>

!!! tldr "TL;DR"
  - [**Как читать документацию**](howto.ru.md)
  - [**Ответы на потенциальные вопросы**](faq.ru.md)
  - [**С чего начать**](quickstart.ru.md)
  - [**Перейти к документации**](errors.md)

<h1 align="center">Мини-карта Python-Multibar</h1>

<div class="mermaid">
    classDiagram
    PInterface <|-- ProgressbarWriter : Implements
    SAbstraction <|-- Sector : Implements
    CAbstraction <|-- CalculationService : Implements
    SignatureSegment <-- Signature : Uses by default
    Signature --> PSProtocol : Matches
    SignatureSegment --> SSProtocol : Matches
    Sector --o ProgressbarWriter : By default
    CalculationService --o ProgressbarWriter : By default
    Signature --o ProgressbarWriter : By default
    PCInterface <|-- ProgressbarClient : Implements
    HInterface <|-- Hooks : Implements
    CMInterface <|-- ContractManager : Implements
    CMInterface --> ContractInterface : Interacts with
    Hooks --o ProgressbarClient : By default
    ContractManager --o ProgressbarClient : By default
    ProgressbarWriter --o ProgressbarClient : By default
</div>
