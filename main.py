import os
import discord
from discord.ext import commands
import io

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')

client = discord.Client()

bot = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print(f'logged in as {client.user}')


@client.event
async def on_message(msg):
    print(msg.author)
    print(f' > {msg.content}')

    if msg.reference != None:
      print(f' > {msg.reference}')      

    if msg.author == client.user:
        return

    if msg.content == '$quoteBot':
        await msg.channel.send('pong')
        return

client.run(TOKEN)

@bot.command(name = 'Add quote')
async def addQuote(ctx, msgID: int): # yes, you can do msg: discord.Message
                                   # but for the purposes of this, i'm using an int

  msg = await ctx.fetch_message(msgID) # you now have the message object from the id
                                         # ctx.fetch_message gets it from the channel
                                         # the command was executed in


bot.run(TOKEN)