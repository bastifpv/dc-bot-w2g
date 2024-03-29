import discord
import json
import requests
import os
from discord import app_commands

TOKEN = os.environ['DCTOKEN']
WKEY = os.environ['W2GTOKEN']
W2GKEYS = {}

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced= False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            
            self.synced = True
        print(f"We have logged in as {self.user}.")


bot = client()
tree = app_commands.CommandTree(bot)


@tree.command(name = 'w2link', description='Create W2G Room with preloaded Video')
async def createRoom(interaction: discord.Interaction, link: str):
    yt_link = link
    url = 'https://api.w2g.tv/rooms/create.json'
    headers = {'Accept':'application/json','Content-Type':'application/json'}
    data = {'w2g_api_key':WKEY,'share':yt_link,'bg_color':'#133857','bg_opacity':"100"}
    data = requests.post(url=url , headers=headers , params=data).json()
    streamkey = data['streamkey']
    embed=discord.Embed(title="W2G Room Link",  url='https://w2g.tv/' + streamkey, color=0x133857)
    embed.add_field(name="Roomkey: ", value=streamkey, inline=True)
    W2GKEYS[interaction.channel.id] = streamkey
    await interaction.response.send_message(embed=embed)

@tree.command(name = 'w2room', description='Create W2G Room')
async def createRoom(interaction: discord.Interaction):
    yt_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    url = 'https://api.w2g.tv/rooms/create.json'
    headers = {'Accept':'application/json','Content-Type':'application/json'}
    data = {'w2g_api_key':WKEY,'share':yt_link,'bg_color':'#133857','bg_opacity':"100"}
    data = requests.post(url=url , headers=headers , params=data).json()
    streamkey = data['streamkey']
    embed=discord.Embed(title="W2G Room Link",  url='https://w2g.tv/' + streamkey, color=0x133857)
    embed.add_field(name="Roomkey: ", value=streamkey, inline=True)
    W2GKEYS[interaction.channel.id] = streamkey
    await interaction.response.send_message(embed=embed)

@tree.command(name = 'w2add', description='Updates W2G Room')
async def createRoom(interaction: discord.Interaction, link: str):
    print(W2GKEYS)
    newLink = link
    try:
        streamkey = W2GKEYS[interaction.channel.id]
        print(streamkey)
    except KeyError:
        error=discord.Embed(title="No room found",  url='https://dino.reuther05.de', color=0x133857)
        error.add_field(name="No room found in this channel: ", value="please use !w2g <link>", inline=False)
        await interaction.response.send_message(embed=error)
        return 
    if len(newLink) == 0:
        error=discord.Embed(title="W2G Room Link",  url='https://w2g.tv/' + streamkey, color=0x133857)
        error.add_field(name="No link found in command: ", value="please use !w2add <link>", inline=False)
        await interaction.response.send_message(embed=error)
        return 
    yt_link = newLink
    url = 'https://api.w2g.tv/rooms/' + streamkey +'/sync_update'
    headers = {'Accept':'application/json','Content-Type':'application/json'}
    data = {'w2g_api_key':WKEY,'item_url':yt_link}
    try:
        requests.post(url=url , headers=headers , params=data).json()
    except:
        print()
    update=discord.Embed(title="W2G Room Link",  url='https://w2g.tv/' + streamkey, color=0x133857)
    update.add_field(name="Room updated: ", value=streamkey, inline=False)
    await interaction.response.send_message(embed=update)

@tree.command(name = 'btc', description='get current btc/usd value')
async def getBTC(interaction: discord.Interaction):
    url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    r = requests.get(url)
    val = str(round(float(r.json().get('price')), 2))
    embed=discord.Embed(title="BTC - USD Kurs")
    embed.add_field(name="current value", value="$" + val, inline=True)
    await interaction.response.send_message(embed=embed)

@tree.command(name = 'meme', description='get random meme')
async def getmeme(interaction: discord.Interaction):
    url = 'https://meme-api.com/gimme'
    r = requests.get(url)
    val = str(r.json().get('url'))
    embed=discord.Embed(title="random meme")
    embed.set_image(url=val)
    await interaction.response.send_message(embed=embed)

@tree.command(name = 'cat', description='get random cat image')
async def getmeme(interaction: discord.Interaction):
    url = 'https://api.thecatapi.com/v1/images/search'
    r = requests.get(url)
    val = str(r.json()[0].get('url'))
    embed=discord.Embed(title="Cat")
    embed.set_image(url=val)
    await interaction.response.send_message(embed=embed)

@tree.command(name = 'dog', description='get random dog image')
async def getmeme(interaction: discord.Interaction):
    url = 'https://dog.ceo/api/breeds/image/random'
    r = requests.get(url)
    val = str(r.json().get('message'))
    embed=discord.Embed(title="Dog")
    embed.set_image(url=val)
    await interaction.response.send_message(embed=embed)


bot.run(TOKEN)