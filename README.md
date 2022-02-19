
<div align="center">
    <a href="https://media.giphy.com/media/Inc6xnOHET6BNOeCfk/giphy.gif?cid=790b761165e4f51105f552cf120a6046e5a4037f28a994ef&rid=giphy.gif&ct=g"><img height="120" width="1920" alt="" src="https://media.giphy.com/media/Inc6xnOHET6BNOeCfk/giphy.gif?cid=790b761165e4f51105f552cf120a6046e5a4037f28a994ef&rid=giphy.gif&ct=g"></a>

<a href="https://github.com/psf/black"><img height="20" alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pycqa.github.io/isort/"><img height="20" alt="Isort" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>
<a href="https://pypi.org/project/python-multibar/"><img height="20" alt="Pypi" src="https://img.shields.io/pypi/v/python-multibar"></a>
<br>
<a href="https://pypi.org/project/python-multibar/"><img height="20" alt="Flake8" src="https://img.shields.io/badge/flake8-checked-blue.svg"></a>
<a href="https://pypi.org/project/mypy/"><img height="20" alt="Mypy badge" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>
<a href="https://pypi.org/project/python-multibar/"><img height="20" alt="Versions" src="https://img.shields.io/pypi/pyversions/python-multibar"></a>

</div>
<div align="center">
    <a href="https://discord.com/invite/KKUFRZCt4f"><img src="https://discordapp.com/api/guilds/744099317836677161/widget.png?style=banner2" alt="" /></a>
</div>

# 👋 Content
- [Installation](#-installation)
    - [Using github](#-using-github)
    - [Using pypi](#-using-pypi)
- [Quickstart](#-quickstart)
- [Useful links](#-useful-links)
  - [Documentation](#-documentation)
  - [Pypi](#-pypi)
  - [Changelog](#-changelog)

----------------------------------------

## ⚙️ Installation
#### ● Using github
```bash
$ pip3 install -U git+https://github.com/Animatea/python-multibar.git#main
```
#### ● Using pypi
```bash
$ pip3 install -U python-multibar
```

## ⚡️ Quickstart
```py
>>> from multibar import ProgressBar

>>> progress = ProgressBar(50, 100).write_progress(fill="+", line="-")
>>> progress.bar
'++++++++++----------'

>>> progress.bar[0].position
0
```

## 🔗 Useful links
#### 📚 documentation
> [click here](https://animatea.github.io/python-multibar/)
#### 📦 pypi
> [click here](https://pypi.org/project/python-multibar/)
#### 📂 changelog
> [click here](https://github.com/Animatea/python-multibar/CHANGELOG.md)
