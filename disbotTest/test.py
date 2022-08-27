from ast import alias
import discord
from discord.ext import commands
from discord import Colour
import asyncio
from discord.ext import tasks

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

app = commands.Bot(command_prefix='!', description=description, intents=intents)

@app.event
async def on_ready():
    print(f'{app.user.name} 연결 성공')
    await app.change_presence(status=discord.Status.online, activity=None)

@app.command(aliases=['이름'])
async def name_msg(ctx):

    await ctx.channel.send(f'{ctx.message.author.name}')
    if ctx.message.author.name == True:
        print('test')
        print(f'{ctx.message.author.name}')


app.run('MTAxMjUxNzMzMTIzNjI5MDY0MA.Gtav1D.DLkhREEhDTDCmIKIWas3MNT43sCOuMhk3MFdRU')
