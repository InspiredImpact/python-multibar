<div id="top"></div>
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
    <a href="https://animatea.github.io/python-multibar/">Documentation</a>
    ·
    <a href="https://github.com/Animatea/python-multibar/issues">Report Bug</a>
    ·
    <a href="https://github.com/Animatea/python-multibar/issues">Request Feature</a>
    </p>
<div id="top"></div>
<p align="center">
   <a href="i18n/ua_README.md"><img height="20" src="https://img.shields.io/badge/language-ua-green?style=social&logo=googletranslate"></a>
   <a href="i18n/ru_README.md"><img height="20" src="https://img.shields.io/badge/language-ru-green?style=social&logo=googletranslate"></a>
</p>
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#welcome-to-python-multibar!">Welcome to Python-Multibar</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#quickstart">Quickstart</a></li>
        <li><a href="#documentation">Documentation</a></li>
        <li><a href="#examples">Examples</a></li>
      </ul>
    </li>
    <li>
      <a href="#contributing">Contributing</a>
    </li>
    <li>
      <a href="#acknowledgments">Acknowledgments</a>
    </li>
  </ol>
</details>

# Welcome to Python-Multibar!
<a href="https://dl.circleci.com/status-badge/redirect/gh/Animatea/python-multibar/tree/main"><img height="20" src="https://dl.circleci.com/status-badge/img/gh/Animatea/python-multibar/tree/main.svg?style=svg"></a>
<a href="https://pypi.org/project/tense/"><img height="20" alt="PyPi" src="https://img.shields.io/pypi/v/python-multibar"></a>
<a href="https://pypi.org/project/mypy/"><img height="20" alt="Mypy badge" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>
<a href="https://github.com/psf/black"><img height="20" alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pycqa.github.io/isort/"><img height="20" alt="Supported python versions" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>

### Installation
```py
# Unix/macOS users should use
$ python -m pip install -U python-multibar

# Windows users should use
$ py -m pip install -U python-multibar
```
### Quickstart
```py
>>> import multibar

>>> writer = multibar.ProgressbarWriter()
>>> progressbar = writer.write(10, 100)
# Using __str__() method, we get a progressbar
# with a basic signature.
Out: '+-----'

# Writer returns progressbar object.
>>> type(progressbar)
Out: <class 'multibar.impl.progressbars.Progressbar'>
```
### Documentation
You can access the documentation by clicking on the following link:
- [animatea.github.io/python-multibar](animatea.github.io/python-multibar/)

### Examples
Some more of the features of python-multibar are in the project examples.
<p align="center">
<br />
<a href="https://github.com/Animatea/python-multibar/tree/main/examples">Python-Multibar Examples</a>
</p>
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

> `NOTE:` before creating a pull request, you first need to install the project's dependencies:
>  - `pip3 install -r dev-requirements.txt -r requirements.txt`
>
> Then go to the root directory of the project `...\python-multibar>` and start all nox pipelines using the `nox` command.
>
> If all sessions are completed successfully, then feel free to create a pull request. Thanks for your PR's!

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Acknowledgments
* [Choose an Open Source License](https://choosealicense.com)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Python](https://www.python.org)
* [Python Community](https://www.python.org/community/)
* [MkDocs](https://www.mkdocs.org)
* [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

