import asyncio

from globalvars import *
from game import GameRoom


async def create_match(msg):
  if msg.author in current_players:
    await client.send_message(msg.channel, 'Please quit your current match first! Use `hm>quit` to quit a match.')

  text = msg.content.lower().split(' ')
  text.pop(0) ## remove the command word

  Room = GameRoom(channel=msg.channel)
  await Room.join(msg.author)

  args = {
    'name' : Room.name,
    'players': Room.max_players,
    'passwd' : Room.password
  }

  for arg in text:
    var, value = arg.split('=',1)
    if var == 'name':
      Room.name = value

  if Room.name == None:
    await client.send_message(msg.channel, 'You must assign your room a name.')

  for item in games:
    if item.name == Room.name:
      await client.send_message(msg.channel, 'The name {} is currently in use. Please select another name.'.format(Room.name))
      return

  try:
    await Room.update_vars()

  except:
    await client.send_message(msg.channel, 'There was an error creating your room. Please check the @help manual for correct command usage')
    return

  games.append(Room)
