<h1 align="center">Python-Multibar</h1>
<p align="center">
<a href="https://dl.circleci.com/status-badge/redirect/gh/Animatea/python-multibar/tree/main"><img height="20" src="https://dl.circleci.com/status-badge/img/gh/Animatea/python-multibar/tree/main.svg?style=svg"></a>
<a href="https://pypi.org/project/python-multibar/"><img height="20" alt="PyPi" src="https://img.shields.io/pypi/v/python-multibar"></a>
<a href="https://pypi.org/project/mypy/"><img height="20" alt="Mypy badge" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>
<a href="https://github.com/psf/black"><img height="20" alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pycqa.github.io/isort/"><img height="20" alt="Supported python versions" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>
</p>

# :gear: Installation
<div class="tabbed-set tabbed-alternate" data-tabs="1:3"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><input id="__tabbed_1_2" name="__tabbed_1" type="radio" /><input id="__tabbed_1_3" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Install with PyPi</label><label for="__tabbed_1_2">Install with Poetry</label><label for="__tabbed_1_3">Install with Git+Pip</label></div>
<div class="tabbed-content">
<div class="tabbed-block">
<p>

```pyсon hl_lines="2 5"
# Unix/macOS users should use
$ python -m pip install -U python-multibar

# Windows users should use
$ py -m pip install -U python-multibar
```

</p>
</div>
<div class="tabbed-block">
<p>

```pycon hl_lines="1"
$ poetry add python-multibar
```
</p>
</div>
<div class="tabbed-block">
<p>

```pycon hl_lines="2 5"
# Unix/macOS users should use
$ python -m pip install git+https://github.com/Animatea/python-multibar.git

# Windows users should use
$ py -m pip install git+https://github.com/Animatea/python-multibar.git
```

</p>
</div>
</div>
</div>

# :gear: Style
> Python-Multibar, like many other projects, has its own code style, which we will describe below.

## :pencil: Code
> For `code` formatting we use [`black`](https://github.com/psf/black),
the configuration of which is in [`pyproject.toml`](https://github.com/Animatea/python-multibar/blob/main/pyproject.toml)

> For `imports` formatting we use [`isort`](https://github.com/PyCQA/isort),
the configuration of which is in [`pyproject.toml`](https://github.com/Animatea/python-multibar/blob/main/pyproject.toml)

>For static `annotations` check we use [`mypy`](https://github.com/python/mypy),
the configuration of which is in [`pyproject.toml`](https://github.com/Animatea/python-multibar/blob/main/pyproject.toml)

>For static `code` check we use [`flake8`](https://github.com/PyCQA/flake8),
the configuration of which is in [`pyproject.toml`](https://github.com/Animatea/python-multibar/blob/main/pyproject.toml)

## :pencil: Docstrings
> For docstrings we use [`numpy doctstring style`](https://numpydoc.readthedocs.io/en/latest/format.html)

<br/>

# :gear: Contributing
`Contributions` are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again! :octicons-heart-fill-24:{ .heart }

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

> `NOTE:` before creating a pull request, you first need to install the project's dependencies:
  ```bash
  pip3 install -r dev-requirements.txt -r requirements.txt
  ```

> Then go to the root directory of the project `...\python-multibar>` and start all nox pipelines using the `nox` command.

> If all sessions are completed successfully, then feel free to create a pull request. Thanks for your PR's!
