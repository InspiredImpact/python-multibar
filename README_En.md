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
