<h1 align="center">Welcome to Python-Multibar!</h1>

<img src="https://media.giphy.com/media/UeRFyF2fJcfnwjVkIn/giphy.gif" align="left" width="200px"/>

Project: python-multibar
<br>
License: Apache 2.0
<br>
About: Tool for static progress bars writing.
<br>
OS: Independent
<br>
Python: 3.9+
<br>
Typing: Typed
<br>
Topic: Utilities
<br />
    <p align="center">
    <br />
    <a href="https://pypi.org/project/python-multibar/">We are on PyPi</a>
    ·
    <a href="https://github.com/Animatea/python-multibar/issues">Report Bug</a>
    ·
    <a href="https://github.com/Animatea/python-multibar/issues">Request Feature</a>
    </p>

!!! nav-menu "Navigation menu"
[**FAQ**](faq.md){ .md-button }
[**Quickstart**](quickstart.md){ .md-button }
[**Showcase**](showcase.md){ .md-button }
[**Python-Multibar**](about.md){ .md-button }
[**Docs**](errors.md){ .md-button }

<h1 align="center">Python-Multibar Minimap</h1>

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

<h1 align="center">Acknowledgments</h1>
<p align="center">
<a href="https://choosealicense.com">Choose an Open Source License</a>
<br/>
<a href="https://shields.io">Img Shields</a>
<br/>
<a href="https://pages.github.com">GitHub Pages</a>
<br/>
<a href="https://www.python.org">Python</a>
<br/>
<a href="https://www.python.org/community/">Python Community</a>
<br/>
<a href="https://www.mkdocs.org">MkDocs</a>
<br/>
<a href="https://squidfunk.github.io/mkdocs-material/">MkDocs Material</a>
<br/>
<a href="https://github.com/fralau/mkdocs-mermaid2-plugin">MkDocs mermaid2</a>
<br/>
<a href="https://github.com/facelessuser/pymdown-extensions">MkDocs pymdown</a>
<br/>
<a href="https://github.com/mkdocstrings/python">MkDocs mkdocstrings</a>
<br/>
<a href="https://mkdocstrings.github.io/autorefs/">MkDocs auto-refs</a>
<br/>
<a href="https://github.com/daxartio/termynal">Mkdocs termynal</a>
<br/>
<a href="https://github.com/facelessuser">Isaac Muse</a>
<br/>
</p>
