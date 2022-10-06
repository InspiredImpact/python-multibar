<div id="top"></div>
<img src="../assets/python-multibar-logo.jpg" align="left" width="200px"/>
Проєкт: python-multibar
<br>
Ліцензія: Apache 2.0
<br>
Опис: Інструмент для статичної генерації прогресбарів.
<br>
ОС: Незалежний
<br>
Python: 3.9+
<br>
Typing: Typed
<br>
Тема: Утиліти
<br />
    <p align="center">
    <br />
    <a href="https://animatea.github.io/python-multibar/">Документація</a>
    ·
    <a href="https://github.com/Animatea/python-multibar/issues">Сповістити про баг</a>
    ·
    <a href="https://github.com/Animatea/python-multibar/issues">Запропонувати ідею</a>
    </p>
<div id="top"></div>
<p align="center">
   <a href="i18n/ua_README.md"><img height="20" src="https://img.shields.io/badge/language-ua-green?style=social&logo=googletranslate"></a>
   <a href="i18n/ru_README.md"><img height="20" src="https://img.shields.io/badge/language-ru-green?style=social&logo=googletranslate"></a>
</p>
<details>
  <summary>Зміст</summary>
  <ol>
    <li>
      <a href="#ласкаво-просимо-до-python-multibar!">Ласкаво просимо до Python-Multibar!</a>
      <ul>
        <li><a href="#установка">Установка</a></li>
        <li><a href="#швидкий-початок">Швидкий початок</a></li>
        <li><a href="#документація">Документація</a></li>
        <li><a href="#приклади">Приклади</a></li>
      </ul>
    </li>
    <li>
      <a href="#зробити-внесок-у-проєкт">Зробити внесок у проєкт</a>
    </li>
    <li>
      <a href="#подяки">Подяки</a>
    </li>
  </ol>
</details>

# Ласкаво просимо до Python-Multibar!
<a href="https://dl.circleci.com/status-badge/redirect/gh/Animatea/python-multibar/tree/main"><img height="20" src="https://dl.circleci.com/status-badge/img/gh/Animatea/python-multibar/tree/main.svg?style=svg"></a>
<a href="https://pypi.org/project/tense/"><img height="20" alt="PyPi" src="https://img.shields.io/pypi/v/python-multibar"></a>
<a href="https://pypi.org/project/mypy/"><img height="20" alt="Mypy badge" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>
<a href="https://github.com/psf/black"><img height="20" alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pycqa.github.io/isort/"><img height="20" alt="Supported python versions" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>

### Установка
```py
# Користувачі Unix/macOS можуть використовувати
$ python -m pip install -U python-multibar

# Користувачі Windows можуть використовувати
$ py -m pip install -U python-multibar
```
### Швидкий початок
```py
>>> import multibar

>>> writer = multibar.ProgressbarWriter()
>>> progressbar = writer.write(10, 100)
# Використовуючи метод __str__(), ми отримуємо прогресбар
# із базовою сигнатурою.
Out: '+-----'

# Writer повертає об'єкт прогресбару.
>>> type(progressbar)
Out: <class 'multibar.impl.progressbars.Progressbar'>
```
### Документація
Ви можете перейти до документації за наступним посиланням:
- [animatea.github.io/python-multibar](animatea.github.io/python-multibar/)

### Приклади
Деякі інші функції python-multibar містяться в прикладах проєкту.
<p align="center">
<br />
<a href="https://github.com/Animatea/python-multibar/tree/main/examples">Python-Multibar Приклади</a>
</p>
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Зробити внесок у проєкт

Будь-який ваш внесок **дуже цінується**.

Якщо у вас є пропозиція, яка могла б покращити проєкт, створіть форк репозиторію та зробіть пулл реквест.
Ви також можете відкрити issue з тегом «enhancement».
Не забудьте поставити зірку проєкту! Дякую ще раз!

1. Створіть форк проєкту
2. Створіть гілку з назвою, яка у двох словах описує суть доповнення/зміни (`git checkout -b feature/AmazingFeature`)
3. Затвердіть Ваші зміни (`git commit -m 'Add some AmazingFeature'`)
4. Надішліть зміни до гілки (`git push origin feature/AmazingFeature`)
5. Створіть Пулл Реквест

> `NOTE:` Перед створенням пулл реквеста необхідно встановити залежність проєкту:
>  - `pip3 install -r dev-requirements.txt -r requirements.txt`
>
> Потім перейдіть в кореневий каталог проєкту `...\python-multibar>`, та запустіть усі пайплайни nox за допомогою команди `nox`.
>
> Якщо всі сесії завершено успішно, сміливо створюйте пулл реквест. Дякуємо за ваш внесок у проєкт!

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Подяки
* [Choose an Open Source License](https://choosealicense.com)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Python](https://www.python.org)
* [Python Community](https://www.python.org/community/)
* [MkDocs](https://www.mkdocs.org)
* [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
* [MkDocs Community](https://www.mkdocs.org)


<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

