import os
import discord
from discord.ext import commands
import io

from dotenv import load_dotenv
from replit import db

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')

client = discord.Client()

bot = commands.Bot(command_prefix='!')

#accepts quote and adds to replit database
def add_quote(msg):
  if str(msg.id) in db: #database keys must be strings for some reason
    response = "Someone else thought it was stupid too! That quote has already been archived"
  else:
    db[str(msg.id)] = msg.content
    response = "That quote is now recorded forever."
  return response

#TODO, have this add to a xlsx file. might store full message info in class
@bot.command(name='AddQuote', help="Adds a quote to the list of cool quotes.")
async def addQuote(ctx):  

    msg = ctx.message

    if msg.reference != None:
        print(f' > {msg.reference}')
        fchdMsg = await msg.channel.fetch_message(msg.reference.message_id)
        print(f' > {fchdMsg.content}')

        response = "Wow! A great Quote from " + fchdMsg.author.name

        await ctx.send(add_quote(fchdMsg))

    else:
        response = "There is no quote here"

    await ctx.send(response)

bot.run(TOKEN)
