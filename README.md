# MCstatusBot
-----

Discord bot pro status Minecraft serveru.

Discord bot každých 5 minut aktualizuje stav minecraft serveru.

## Zpráva obsahuje
* Název serveru
* MOTD
* IP serveru
* Port serveru
* Status **online/offline**
* Počet hráčů
* Logo serveru


Lokalizace CS/EN  - lze přidat další jazyk

## Config

    "token": "BOT TOKEN",
    "channel_id": "channel ID",
    "server_ip": "server IP",
    "server_port": "server port",
    "language": "cs",
    "show_motd": true,
    "show_ip": true,
    "show_port": true,
    "show_player_count": true,
    "logo_url": "Logo URL"

### Instalace UBUNTU

```console
sudo apt update
sudo apt install python3 python3-pip
pip3 install discord.py requests
pip3 install mcstatus
```


### Spuštění bota

```python
python3 bot.py
```



