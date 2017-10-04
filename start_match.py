from globalvars import *

async def start_match(message):
  for lobby in games:
    if message.author in lobby.players:
      lobby.started = 1
      return
  await client.send_message(message.channel, 'You aren\'t in a match! Use `@help` to access the command list.')
