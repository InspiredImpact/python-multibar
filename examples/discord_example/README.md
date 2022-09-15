<div id="top"></div>
<img src="../../assets/python-multibar-logo.jpg" align="left" width="200px"/>

<h1 align="center">Python-Multibar Examples</h1>
<p align="center">
<br />
<a href="https://github.com/Animatea/python-multibar/tree/main/examples/discord/hikari_tanjun_example">Hikari-Tanjun</a>
·
<a href="https://github.com/Animatea/python-multibar/tree/main/examples/discord/hikari_lightbulb_example">Hikari-Lightbulb</a>
·
<a href="https://github.com/Animatea/python-multibar/tree/main/examples/discord/disnake_example">Disnake</a>
·
<a href="https://github.com/Animatea/python-multibar/tree/main/examples/discord/discord_py_example">Discord.py</a>
</p>

# How To Run
### ● First clone repository
```bash
$ git clone https://github.com/Animatea/python-multibar.git
```

### ● If you want to use exiting implementation (optional caching with JSON)
Rename `data.json.example` to `data.json`
> **Note** that you can quite simply write your own implementations of interfaces
> (
> [`leveling.api.repository.UserRepositoryAware`](https://github.com/Animatea/python-multibar/tree/main/examples/discord/discord_py_example/leveling/api/repository.py),
> [`leveling.api.unit_of_work.AbstractUserUnitOfWork`](https://github.com/Animatea/python-multibar/tree/main/examples/discord/discord_py_example/leveling/api/unit_of_work.py)
> )
> using,
> for example, MongoDB or PostgreSQL etc.

### ● Then:
- Go to examples/discord_example dir
- Run launcher.py file
    - `NOTE:` You can choose and install any launcher in launcher.py, or even create your own.<br/>
      **Currently implemented:**
        - [HikariTanjunLauncher](https://github.com/Animatea/python-multibar/tree/main/examples/discord/discord_py_example/launcher.py)
        - [HikariLightbulbLauncher](https://github.com/Animatea/python-multibar/tree/main/examples/discord/discord_py_example/launcher.py)
        - [DiscordpyLauncher](https://github.com/Animatea/python-multibar/tree/main/examples/discord/discord_py_example/launcher.py)
        - [DisnakeLauncher](https://github.com/Animatea/python-multibar/tree/main/examples/discord/discord_py_example/launcher.py)