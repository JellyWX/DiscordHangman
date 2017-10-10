import asyncio
import discord

from globalvars import *

async def join_match(message):
  if message.author in current_players:
    await client.send_message(message.channel, 'Please quit your current match first! Use `hm>quit` to quit a match.')
    
  text = message.content.lower().split(' ')
  text.pop(0)

  for room in games:
    if room.name == text[0]: ## if the room name matches the text provided

      if room.public: ## if the room has no password
        await room.join(message.author)
        await client.send_message(messae.channel, 'You joined the room {}!'.format(room.name))

      else: ## if the room is password protected
        if len(text) == 1: ## if no password was provided
          await client.send_message(message.channel, 'Room is password-protected. Please enter a password using `@join <room-name> <password>`')

        elif text[1] == room.password: ## if the password is correct
          await room.join(message.author)

        else:
          await client.send_message(message.channel, 'Wrong password. Please try again (passwords are not case sensitive)') ## if the password was otherwise incorrect

      break

  else:
    await client.send_message(message.channel, 'No room found by name provided') ## if the room couldn't be found
