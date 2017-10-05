from globalvars import *

async def content_parser(message):
  #if message.author in [g.active_player for g in games]:
  #  return

  guess = message.content.lower()[1:]

  if message.author in current_players and message.channel in active_channels:
    if alphaStr(guess):
      ## get lobby containing user and send guess
      for lobby in games:
        if not lobby.started:
          return
        if message.author in lobby.players and message.channel == lobby.channel:
          await lobby.process_guess(guess)
          return

    else:
      await client.send_message(message.channel, 'Your guess must be an English letter or word (no spaces).')
