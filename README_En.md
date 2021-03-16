#### 📤 Back to main page | Вернуться на главную
[![InviteToServer](https://img.shields.io/badge/-Main_page-2f3136?style=for-the-badge&logo=github)](https://github.com/Animatea/DiscordProgressbar/blob/main/README.md)

### 📖 Parameters. [] - Required, <> - Optional
|           name            |                     type                    |   Default  |                           Information                               |
|:-------------------------:|:-------------------------------------------:|:----------:|:-------------------------------------------------------------------:|
|          now `[]`         |                    `int`                    |   `None`   | Progress now
|         needed `[]`       |                    `int`                    |   `None`   | Needed progress
|          type `[]`        |               `str (post/get)`              |   `None`   | The type of progressbar that will be returned to you, `get` - will return you a progressbar in string, `post` - add a field to your discord.Embed with progressbar
|    embed `[]` *(optional when type is 'get')* | `discord.Embed`         |   `None`   | Your [discord.Embed](https://discordpy.readthedocs.io/en/latest/api.html#discord.Embed)
|         is_left `<>`      |                    `bool`                   |   `False`  | If True, shows what progress is now from the needed progress, set to the right of the progressbar in the format [100/1000]
|         to_dict `<>`      |                    `dict`                   |   `None`   | This parameter requires discord.Embed, returns you an embed with a progress bar in the dictionary
|        percents `<>`      |                    `bool`                   |   `False`  | Shows the percentage of progress made, set to the right of the progressbar before (is_left), if specified
|       field_name `<>`     |                    `str`                    |`"Progress"`| Changes the name of the added field with a progressbar
|      field_inline `<>`    |                    `bool`                   |   `False`  | Changes the inline of the added field with a progressbar
|     field_position `<>`   |                    `int`                    |   `None`   | Default - sets it as the last field in embed, sets the position of the field in the embed, the counting starts from 0
|      clear_fields `<>`    |                    `bool`                   |   `False`  | Removes all fields from your discord.Embed before adding a field with a progressbar
|    progress() function `[]`|                 `coroutine`                |            | Params:<br>`line` : the character or string that will be a line that we will fill in as progress increases<br> `fill` : the character or string that will fill the line as progress increases.<br>If nothing is specified, then default fill emoji is ":red_square:" and default line emoji is ":black_large_square:"

### 💢 Errors
|         type              |                    cause                    |
|:-------------------------:|:-------------------------------------------:|
|      `MissingArgument`    |   Raised when one of the args is missing    |
|       `BadArgument`       |      Raised when specified bad arg          |
|       `ProgressError`     |      Raised when [now] > [needed]           |
|      `TooLargeArgument`   |      Raised when embed position idx > 25    |
|       `TooManyFields`     | Raised when len(embed fields) + field with progressbar > 25  |
|         `BadEmbed`        |     Raised when embed != discord.Embed()    |
|         `BadType`         |      Raised when type not in [post / get]   |

### Examples

> Simple example of use

```py
from random import randint
import DiscordProgressbar as Bar


@bot.command()
async def progress(ctx):
    embed = discord.Embed()
    pnow, pneed = randint(1, 100), randint(100, 1000)

    progress = await Bar(now=pnow, needed=pneed, embed=embed, type='post').progress()
    return await ctx.send(embed=progress)
```
[![Header](https://github.com/Animatea/DiscordProgressbar/blob/main/assets/example1.png)]()

> More modified

```py
from random import randint
import DiscordProgressbar as Bar


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

> Working with fields and our custom symbols

```py
from random import randint
import DiscordProgressbar as Bar


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

> Clearing existing fields

```py
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
