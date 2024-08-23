import discord
import json
import asyncio
from mcstatus import JavaServer

# Načtení konfigurace
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Načtení lokalizace
with open(f'lang/{config["language"]}.json', 'r') as lang_file:
    lang = json.load(lang_file)

# Nastavení klienta
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# Funkce pro získání statusu Minecraft serveru
def get_minecraft_status():
    try:
        server = JavaServer.lookup(f'{config["server_ip"]}:{config["server_port"]}')
        status = server.status()

        result = {
            "online": True,
            "motd": status.description,
            "player_count": status.players.online,
            "max_players": status.players.max
        }
    except Exception as e:
        result = {"online": False}
    return result

async def update_status_message():
    channel = client.get_channel(int(config['channel_id']))
    message_id = None
    
    async for message in channel.history(limit=100):
        if message.author == client.user:
            message_id = message.id
            break

    status = get_minecraft_status()
    
    embed = discord.Embed(title=lang["server_name"])
    
    if config["show_motd"]:
        embed.add_field(name=lang["motd"], value=status.get("motd", "N/A"), inline=False)
    
    if config["show_ip"]:
        embed.add_field(name=lang["ip"], value=config["server_ip"], inline=True)
    
    if config["show_port"]:
        embed.add_field(name=lang["port"], value=config["server_port"], inline=True)
    
    if status["online"]:
        embed.add_field(name=lang["status_online"], value="🟢 " + lang["status_online"], inline=False)
        if config["show_player_count"]:
            embed.add_field(name=lang["player_count"], value=f'{status["player_count"]}/{status["max_players"]}', inline=True)
    else:
        embed.add_field(name=lang["status_offline"], value="🔴 " + lang["status_offline"], inline=False)
    
    # Přidání loga serveru
    embed.set_thumbnail(url=config["logo_url"])

    # Přidání patičky s textem
    embed.set_footer(text="Coded by AI and JaraSG2")

    # Aktualizace nebo vytvoření nové zprávy
    if message_id:
        message = await channel.fetch_message(message_id)
        await message.edit(embed=embed)
    else:
        message = await channel.send(embed=embed)
        message_id = message.id

    # Přidání tlačítka pro refresh
    button = discord.ui.Button(label=lang["refresh"], style=discord.ButtonStyle.green)

    async def button_callback(interaction):
        if interaction.user == client.user:
            await interaction.response.defer()
            return
        await interaction.response.send_message('Refreshing...', ephemeral=True)
        await update_status_message()

    button.callback = button_callback
    view = discord.ui.View()
    view.add_item(button)
    
    if message_id:
        message = await channel.fetch_message(message_id)
        await message.edit(view=view)
    else:
        message = await channel.send(embed=embed, view=view)
        message_id = message.id

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    await update_status_message()

    while True:
        await asyncio.sleep(300)
        await update_status_message()

client.run(config['token'])
