import os
import discord
from discord.ext import commands
import io
import random

from dotenv import load_dotenv

# TODO figure out if replit allows more than one value per key
from replit import db # user replit db (uses weird json format)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')

client = discord.Client()

bot = commands.Bot(command_prefix='!')

#accepts quote and adds to replit database
#could just store message ID and fetch the message when returning the quote
def add_quote(msg):
  if str(msg.id) in db: #database keys must be strings for some reason
    response = "Someone else thought it was stupid too! That quote has already been archived"
  else:
    db[str(msg.id)] = msg.content
    response = "That quote is now recorded forever."
  return response

def get_quote():
  random.seed()
  entries = db.prefix("")
  msgId = random.choice(entries)

  return int(msgId)


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

#TODO add url and reply to direct quote as well as the quote content.
@bot.command(name='GetQuote', help='Returns a random quote')
async def getQuote(ctx):

  msg = ctx.message
  msgId = get_quote()
  fchdMsg = await msg.channel.fetch_message(msgId)

  response = "Remember when " + fchdMsg.author.name + " said this?!\n"
  response = response + "```" + fchdMsg.content + "```\n" + fchdMsg.jump_url

  await ctx.send(response)

@bot.command(name='ListQuotes', help="Returns how many entires are stored")
async def getLen(ctx):
  numQuotes = str(db.__len__())
  response = "There are " + numQuotes + " stored."
  await ctx.send(response)

bot.run(TOKEN)
