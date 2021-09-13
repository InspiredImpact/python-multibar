<div align="center">
    <a href="https://media.giphy.com/media/Inc6xnOHET6BNOeCfk/giphy.gif?cid=790b761165e4f51105f552cf120a6046e5a4037f28a994ef&rid=giphy.gif&ct=g"><img height="120" width="1920" alt="" src="https://media.giphy.com/media/Inc6xnOHET6BNOeCfk/giphy.gif?cid=790b761165e4f51105f552cf120a6046e5a4037f28a994ef&rid=giphy.gif&ct=g"></a>

![Pypi](https://img.shields.io/pypi/v/python-multibar)
![Versions](https://img.shields.io/pypi/pyversions/python-multibar)
![Mypy](http://www.mypy-lang.org/static/mypy_badge.svg)
[![PEP8](https://img.shields.io/badge/flake8-checked-blue.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![TOTAL LINES](https://img.shields.io/tokei/lines/github/Animatea/python-multibar)
</div>
<div align="center">
    <a href="https://discord.com/invite/KKUFRZCt4f"><img src="https://discordapp.com/api/guilds/744099317836677161/widget.png?style=banner2" alt="" /></a>
</div>

# 👋 Content
- [Installation](#-installation)
    - [Using github](#-using-github)
    - [Using pypi](#-using-pypi)
- [Quickstart](#-quickstart)
- [Flags](#-flags)
- [Useful links](#-useful-links)
  - [Documentation](#-documentation)
  - [Pypi](#-pypi)
  - [Changelog](#-changelog)
- [TODO](#-todo)
- [Contributing](#-contributing)

----------------------------------------

## ⚙️ Installation
#### ● Using github
```bash
$ pip3 install -U git+https://github.com/Animatea/python-multibar.git#master
```
#### ● Using pypi
```bash
$ pip3 install -U python-multibar
```

## ⚡️ Quickstart
```py
import random

from multibar import ProgressBar, ProgressTemplates


bar = ProgressBar(
    random.randint(10, 50),  # Current progress
    random.randint(50, 100),  # Needed progress
)
progress = bar.write_progress(**ProgressTemplates.DEFAULT)
print(f"Your progress: {progress}")
```

## 🏳️ Flags
> In our project flags are used to validate and format code.

Flag   | Description  | Usage  |
------ | ------------ | ------ |
`--mypy` | Checking a project for type-hints using a config file. | `python3 -m multibar --mypy` |
`--flake8` | Checking a project for pep8 using a config file. | `python3 -m multibar --flake8` |
`--black` | Code formatting using config file. | `python3 -m multibar --black`

## 🔗 Useful links
#### 📚 documentation
> [click here](https://app.gitbook.com/@denys111/s/python-multibar/)
#### 📦 pypi
> [click here](https://pypi.org/project/python-multibar/)
#### 📂 changelog
> [click here](https://github.com/Animatea/python-multibar/blob/master/CHANGELOG.md)

## ✅ TODO
- [ ] CLI support

## 📈 Contributing
To get more familiar with the project, you should start by reading the documentation [docs](https://app.gitbook.com/@denys111/s/python-multibar/). If you are already familiar with the project, then you should start by cloning our repository:
```bash
$ git clone https://github.com/Animatea/python-multibar.git
```
Then you create a virtual environment into which you can install any dependencies (`pip3 install -r requirements.txt` | `pip3 install -r dev-requirements.txt`).
Where to begin? See open [issues](https://github.com/Animatea/python-multibar/issues), thanks for your contribution to the project!

**!!! Note:**
We try to write as clear and beautiful code as possible, so before submitting requests, format your code with black and check with mypy, flake8 (using [flags](#-flags)).
