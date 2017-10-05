import asyncio
import discord

from globalvars import *


async def quit_match(message):
  quitter = message.author
  if quitter in current_players:
    for lobby in games:
      if quitter in lobby.players:
        await lobby.quit(quitter)
        current_players.remove(quitter)

  else:
    await client.send_message(message.channel, 'You are not in a match! To join a match, use `hm>join`. To create a match, use `hm>create`')
