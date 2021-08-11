# QuoteBot

This bot connects to a discord and stores quotes as a replit database. It can then return random quotes when asked.

Made it because I wanted to roughly learn the discord.py package and API.

Commands are prefixed with the '!' character, otherwise they will be ignored by the bot.

## Requirements

This was built using replit, and leans on a replit databse (which  is some kind of weird JSON file, idk). So it won't store things unless ran on replit. At some point I'll probably get around to doing it as a csv or something.

It'll also be unhappy if the same instance is used in multiple servers, might try and fetch a message from a different server.

## Commands

### !AddQuote

Checks that the message is replying to another message, then adds the msg.id and content to the databse. If that message has been stored, returns a response letting the user know.

### !GetQuote

Returns a random quote from the stored databse. Does this by retreiving a random message id, fetching that message from the channel and replying to it as well as printing the content.

###  !ListQuotes

Returns the number of stored quotes

### !DelAll

Deletes all stored msgids. Requires the entering of a passkey stored as an environmental variable. 