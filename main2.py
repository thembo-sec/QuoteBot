import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
from tinydb import TinyDB, Query

db = TinyDB('quotedb.json')

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')

client = discord.Client()

bot = commands.Bot(command_prefix='QB ')


def add_quote(msg):
    messages = Query()
    if db.search(messages.id == msg.id):
        response = "Message already exists"
    else:
        db.insert(to_dict(msg))  # store msgid and content in the message
        response = "Wow! A great Quote from " + msg.author.name + "\n"
        response = response + "This'll look good in the pool room"
    return response


def get_quote():
    random.seed()  # set new seed each time its called
    entries = db.prefix("")  # easiest way to get replit db to return all entries
    msgId = random.choice(entries)

    return int(msgId)  # only need id, can just fetch message if only used in 1 channel


def to_dict(msg):
    # This function converts discord message to a dict for storage with tinyDB
    msg_dict = {
        "id": msg.id,
        "author": msg.author.name,
        "content": msg.content
    }
    print(msg_dict)
    return msg_dict


@bot.command(name='AddQuote', help="Adds a quote to the list of cool quotes.")
async def addQuote(ctx):
    msg = ctx.message

    if msg.reference != None:
        print(f' > {msg.reference}')
        fchdMsg = await msg.channel.fetch_message(msg.reference.message_id)

        response = add_quote((fchdMsg))
        print(type(fchdMsg.content))

        await ctx.send(response)

    else:
        response = "There is no quote here"
        await ctx.send(response)


bot.run(TOKEN)
