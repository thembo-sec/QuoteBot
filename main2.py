import os
import random

#test

import discord
from discord.ext import commands
from dotenv import load_dotenv
from tinydb import TinyDB, Query, where

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


def get_quote(msg):
    random.seed()  # set new seed each time its called
    entries = db.search(where('channel') == msg.channel.name)  # get number of entries
    message = random.choice(entries)
    return message


def to_dict(msg):
    # This function converts discord message to a dict for storage with tinyDB
    msg_dict = {
        "id": msg.id,
        "author": msg.author.name,
        "content": msg.content,
        "channel": msg.channel.name
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


@bot.command(name='GetQuote', help='Returns a random quote')
async def getQuote(ctx):
    msg = ctx.message  # assign
    fetched_msg = get_quote(msg)
    fetched_id = fetched_msg.get('id')

    try:
        fchdMsg = await msg.channel.fetch_message(fetched_id)
        response = "Remember when " + fchdMsg.author.name + " said this?!\n"
        response = response + "```" + fchdMsg.content + "```\n"
        await fchdMsg.reply(response)
    except:
        response = "That message doesnt exist?! Was it deleted?"
        await ctx.reply(response)


@bot.command(name='ListQuotes', help="Returns how many entires are stored")
async def getLen(ctx):
    numQuotes = str(len(db))
    response = "There are " + numQuotes + " stored."
    await ctx.send(response)


@bot.command(name='DelAll', help="Deletes all existing quotes.")
async def delAll(ctx, *args):
    if len(args) > 1:
        await ctx.send("Invalid arguments, please enter delete key")
        return
    elif len(args) == 0:
        await ctx.send("Please enter delete key")
        return
    else:
        # make sure the key is an integer
        # could be a str if changed
        try:
            del_key = int(args[0])
        except:
            await ctx.send("The key should be digits only")
            return

    # key stored in environment value rather than hardcoded.
    # *taps head* Cyber Security
    if del_key == int(os.getenv("DEL_KEY")):
        db.truncate()
        await ctx.send("All entries deleted")
    else:
        await ctx.send("Please enter the correct password to delete all entries")


bot.run(TOKEN)
