#### 📤 Вернуться на главную | Back to main page
[![InviteToServer](https://img.shields.io/badge/-Main_page-2f3136?style=for-the-badge&logo=github)](https://github.com/Animatea/DiscordProgressbar/blob/main/README.md)

### 📖 Параметры. [] - Обязательный, <> - Необязательный
|           Название            |                     Тип                    |   Стандартное значение  |                           Информация                               |
|:-------------------------:|:-------------------------------------------:|:----------:|:-------------------------------------------------------------------:|
|          now `[]`         |                    `int`                    |   `None`   | Прогресс сейчас
|         needed `[]`       |                    `int`                    |   `None`   | Необходимый прогресс (сколько нужно прогресса в общем)
|          type `[]`        |               `str (post/get)`              |   `None`   | Тип прогрессбара который будет вам возвращён, `get` - вернёт вам прогрессбар строкой, `post` - добавит поле к вашему discord.Embed
|    embed `[]` *(необязателен когда установлен тип 'get')* | `discord.Embed`         |   `None`   | Ваш [discord.Embed](https://discordpy.readthedocs.io/en/latest/api.html#discord.Embed)
|         is_left `<>`      |                    `bool`                   |   `False`  | Если True, показывает сколько прогресса сейчас из прогресса в общем, устанавливается справа от прогрессбара в формате [100/1000]
|         to_dict `<>`      |                    `bool`                   |   `False`   | Для этого параметра необходим discord.Embed, возвращает вам эмбед с прогрессбаром в словаре
|        percents `<>`      |                    `bool`                   |   `False`  | Показывает на сколько процентов продвинулся прогресс, устаналивается справа от прогрессбара до (is_left), если тот указан
|       field_name `<>`     |                    `str`                    |`"Progress"`| Меняет имя добавляемого поля с прогрессбаром
|      field_inline `<>`    |                    `bool`                   |   `False`  | Меняет inline поля с прогрессбаром
|     field_position `<>`   |                    `int`                    |   `None`   | Стандартно устанавливает самым последним полем в эмбеде. Устанавливает поле с прогрессбаром в вашем эмбеде на определённую позицию по индексу, счёт ведётся с 0
|      clear_fields `<>`    |                    `bool`                   |   `False`  | Удаляет уже все существующие поля с вашего эмбеда прежде чем добавить поле с прогрессбаром
|    progress() функция `[]`|                 `coroutine`                |            | Параметры:<br>`line` : символ линии, которую будем заполнять по мере продвижения прогресса<br> `fill` : символ, которым будем заполнять линию по мере продвижения прогресса.<br>Если ничего не указать, то стандартным символом для заполению линии будет ":red_square:" и стандартным символом линии для будет ":black_large_square:"

### 💢 Errors
|         Тип              |                    Причина                    |
|:-------------------------:|:-------------------------------------------:|
|      `MissingArgument`    |   Вызывается, когда не указан один из необходимых элементов    |
|       `BadArgument`       |      Вызывается, когда указан неверный аргумент         |
|       `ProgressError`     |      Вызывается, когда [now] > [needed] (прогресс сейчас не может быть больше нужного)           |
|      `TooLargeArgument`   |     Вызывается, когда параметр field_position > 25    |
|       `TooManyFields`     | Вызывается, когда len(embed fields) + поле с прогрессбаром > 25  |
|         `BadEmbed`        |     Вызывается, когда embed != discord.Embed()    |
|         `BadType`         |      Вызывается, когда указан не верный тип, доступные: post, get   |

### Examples

> Простой пример использования

```py
from random import randint
from DiscordBar import DSprogressbar as Bar


@bot.command()
async def progress(ctx):
    embed = discord.Embed()
    pnow, pneed = randint(1, 100), randint(100, 1000)

    progress = await Bar(now=pnow, needed=pneed, embed=embed, type='post').progress()
    return await ctx.send(embed=progress)
```
[![Header](https://github.com/Animatea/DiscordProgressbar/blob/main/assets/example1.png)]()

> Более продвинутый вариант

```py
from random import randint
from DiscordBar import DSprogressbar as Bar


@bot.command()
async def progress(ctx):
    embed = discord.Embed()
    pnow, pneed = randint(1, 100), randint(100, 1000)
    name = "My Custom Name Of The Progressbar"

    progress = await Bar(now=pnow, needed=pneed, embed=embed, type='post',
                        is_left=True, percents=True, field_name=name).progress()

    return await ctx.send(embed=progress)
```
[![Header](https://github.com/Animatea/DiscordProgressbar/blob/main/assets/example2.png)]()

> Работа с полями и собственными символами для прогрессбара

```py
from random import randint
from DiscordBar import DSprogressbar as Bar


@bot.command()
async def progress(ctx):
    embed = discord.Embed()

    fields = [ # our fields
        ('name_1', 'value_1', True),
        ('name_2', 'value_2', False),
        ('name_3', 'value_3', False),
        ('name_4', 'value_4', False),
        ('name_5', 'value_5', False),
    ]
    for name, value, inline in fields: # add fields
        embed.add_field(name=name, value=value, inline=inline)

    pnow, pneed = randint(1, 100), randint(100, 1000)

    name = "My Custom Name Of The Progressbar"
    fill_emoji = '<:fill_bar:784863727463170068>'
    line_emoji = '<:line_bar:784864314552352768>'

    bar = Bar(now=pnow, needed=pneed, embed=embed,
                type='post', is_left=True, percents=True,
                field_name=name, field_inline=True, field_position=0)

    progress = await bar.progress(fill=fill_emoji, line=line_emoji)
    return await ctx.send(embed=progress)
```
We got 2 fields in a row, because the first field in the list has inline=True and we also set the parameter field_inline=True
[![Header](https://github.com/Animatea/DiscordProgressbar/blob/main/assets/example3.png)]()

> Очистка уже существующих полей

```py
from random import randint
from DiscordBar import DSprogressbar as Bar


@bot.command()
async def progress(ctx):
    embed = discord.Embed()

    embed.add_field(name='1', value='1')
    embed.add_field(name='2', value='2')
    embed.add_field(name='3', value='3')

    pnow, pneed = randint(1, 100), randint(100, 1000)

    name = "My Custom Name Of The Progressbar"
    fill_emoji = '<:fill_bar:784863727463170068>'
    line_emoji = '<:line_bar:784864314552352768>'

    bar = Bar(now=pnow, needed=pneed, embed=embed,
                type='post', is_left=True, percents=True,
                field_name=name, clear_fields=True)
                # cleared all already existing fields

    progress = await bar.progress(fill=fill_emoji, line=line_emoji)
    return await ctx.send(embed=progress)
```
[![Header](https://github.com/Animatea/DiscordProgressbar/blob/main/assets/example4.png)]()

> Конвертирует эмбед с прогрессбаром в словарь

```py
from random import randint
from DiscordBar import DSprogressbar as Bar


@bot.command()
async def progress(ctx):
    embed = discord.Embed(
        title = 'Embed title',
        description = 'Some description',
        color = 0x2f3136
    )

    pnow, pneed = randint(1, 100), randint(100, 1000)

    bar = Bar(now=pnow, needed=pneed, embed=embed,
                type='post', percents=True, to_dict=True)

    progress = await bar.progress(fill='+', line='-')
    return await ctx.send(progress)
```
[![Header](https://github.com/Animatea/DiscordProgressbar/blob/main/assets/example5.png)]()

> И ещё пару слов о методе "get"

```py
from random import randint
from DiscordBar import DSprogressbar as Bar


@bot.command()
async def progress(ctx):
    pnow, pneed = randint(1, 100), randint(100, 1000)

    bar = Bar(now=pnow, needed=pneed, type='get')
    progress = await bar.progress(line='-', fill='+')

    return await ctx.send(
        f"Progress now:\n {progress}"
    )
```
[![Header](https://github.com/Animatea/DiscordProgressbar/blob/main/assets/example6.png)]()
