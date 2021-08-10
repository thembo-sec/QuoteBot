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

@bot.command(name='AddQuote', help="Adds a quote to the list of cool quotes.")
async def addQuote(ctx):  # yes, you can do msg: discord.Message
    # but for the purposes of this, i'm using an int

    msg = ctx.message

    if msg.reference != None:
        print(f' > {msg.reference}')
        fchdMsg = await msg.channel.fetch_message(msg.reference.message_id)
        print(f' > {fchdMsg.content}')

        response = "Wow! A great Quote"

    else:
        response = "There is no quote here"

    await ctx.send(response)

bot.run(TOKEN)
