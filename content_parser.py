from globalvars import *

async def content_parser(message):
  guess = message.content.lower()

  if message.author in current_players and message.channel in active_channels:
    if alphaStr(guess):
      ## get lobby containing user and send guess
      for lobby in games:
        if message.author in lobby.players and message.channel == lobby.channel:
          await lobby.process_guess(guess)
          return

    else:
      await client.send_message(message.channel, 'Your guess must be an English letter or word (no spaces).')
