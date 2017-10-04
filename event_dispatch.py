import asyncio
import discord

from globalvars import *


async def event_dispatch():
  await client.wait_until_ready()
  while not client.is_closed:

    ## first, delete any empty lobbies
    for lobby in games:
      if len(lobby.players) == 0: #or (len(lobby.players) == 1 and lobby.word != ''):
        games.remove(lobby)
        del lobby
        continue

      if lobby.closed:
        for player in lobby.players:
          current_players.remove(player)

        games.remove(lobby)
        del lobby
        continue

      if lobby.word == '' and lobby.started:
        await lobby.set_word()

    await asyncio.sleep(0.4)
