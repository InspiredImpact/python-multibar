<div id="top"></div>
<img src="../assets/python-multibar-logo.jpg" align="left" width="200px"/>
Проект: python-multibar
<br>
Лицензия: Apache 2.0
<br>
Описание: Инструмент для статической генерации прогрессбаров.
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
    <a href="https://animatea.github.io/python-multibar/">Документация</a>
    ·
    <a href="https://github.com/Animatea/python-multibar/issues">Сообщить о баге</a>
    ·
    <a href="https://github.com/Animatea/python-multibar/issues">Предложить идею</a>
    </p>
<div id="top"></div>
<p align="center">
   <a href="i18n/ua_README.md"><img height="20" src="https://img.shields.io/badge/language-ua-green?style=social&logo=googletranslate"></a>
   <a href="i18n/ru_README.md"><img height="20" src="https://img.shields.io/badge/language-ru-green?style=social&logo=googletranslate"></a>
</p>
<details>
  <summary>Оглавление</summary>
  <ol>
    <li>
      <a href="#добро-пожаловать-в-python-multibar!">Добро пожаловать в Python-Multibar!</a>
      <ul>
        <li><a href="#установка">Установка</a></li>
        <li><a href="#быстрый старт">Быстрый старт</a></li>
        <li><a href="#документация">Документация</a></li>
        <li><a href="#примеры">Примеры</a></li>
      </ul>
    </li>
    <li>
      <a href="#сделать-вклад-в-проект">Сделать вклад в проект</a>
    </li>
    <li>
      <a href="#благодарности">Благодарности</a>
    </li>
  </ol>
</details>

# Добро пожаловать в Python-Multibar!
<a href="https://dl.circleci.com/status-badge/redirect/gh/Animatea/python-multibar/tree/main"><img height="20" src="https://dl.circleci.com/status-badge/img/gh/Animatea/python-multibar/tree/main.svg?style=svg"></a>
<a href="https://pypi.org/project/tense/"><img height="20" alt="PyPi" src="https://img.shields.io/pypi/v/python-multibar"></a>
<a href="https://pypi.org/project/mypy/"><img height="20" alt="Mypy badge" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>
<a href="https://github.com/psf/black"><img height="20" alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pycqa.github.io/isort/"><img height="20" alt="Supported python versions" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>

### Установка
```py
# Пользователи Unix/macOS могут использовать
$ python -m pip install -U python-multibar

# Пользователи Windows могут использовать
$ py -m pip install -U python-multibar
```
### Быстрый старт
```py
>>> import multibar

>>> writer = multibar.ProgressbarWriter()
>>> progressbar = writer.write(10, 100)
# Используя __str__() метод, мы получаем прогрессбар
# с базовой сигнатурой.
Out: '+-----'

# Writer возвращает объект прогрессбара.
>>> type(progressbar)
Out: <class 'multibar.impl.progressbars.Progressbar'>
```
### Документация
Вы можете приступить к документации, перейдя по следующей ссылке:
- [animatea.github.io/python-multibar](animatea.github.io/python-multibar/)

### Примеры
Some more of the features of python-multibar are in the project examples.
<p align="center">
<br />
<a href="https://github.com/Animatea/python-multibar/tree/main/examples">Python-Multibar Примеры</a>
</p>
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Сделать вклад в проект

Любой ваш вклад **очень ценится**.

Если у вас есть предложение, которое могло бы улучшить проект, создайте форк репозитория и создайте пулл реквест.
Вы также можете просто открыть issue с тегом «enhancement».
Не забудьте поставить звезду проекту! Спасибо ещё раз!

1. Создайте форк проекта
2. Создайте ветку с названием, которое в двух словах описывает суть дополнения/изменения (`git checkout -b feature/AmazingFeature`)
3. Подтвердите Ваши изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте изменения на ветку (`git push origin feature/AmazingFeature`)
5. Создайте Пулл Реквест

> `NOTE:` перед созданием пулл реквеста необходимо установить зависимости проекта:
>  - `pip3 install -r dev-requirements.txt -r requirements.txt`
>
> Затем перейдите в корневой каталог проекта `...\python-multibar>` и запустите все пайплайны nox с помощью команды `nox`.
>
> Если все сессии завершены успешно, смело создавайте пулл реквест. Спасибо за ваш вклад в проект!

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Благодарности
* [Choose an Open Source License](https://choosealicense.com)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Python](https://www.python.org)
* [Python Community](https://www.python.org/community/)
* [MkDocs](https://www.mkdocs.org)
* [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
* [MkDocs Community](https://www.mkdocs.org)

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

