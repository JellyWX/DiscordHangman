import discord
import asyncio

from sys import argv

from globalvars import *

from join_match import join_match
from create_match import create_match
from start_match import start_match
from quit_match import quit_match
from event_dispatch import event_dispatch
from content_parser import content_parser


@client.event ## print some stuff to console when the bot is activated
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.change_presence(game=discord.Game(name='hangman'))

@client.event
async def on_message(message):
  if message.content in ['', None] or message.author == client.user:
    return

  if message.content.startswith('@create'):
    await create_match(message)

  elif message.content.startswith('@join'):
    await join_match(message)

  elif message.content.startswith('@quit'):
    await quit_match(message)

  elif message.content.startswith('@start'):
    await start_match(message)

  else:
    await content_parser(message)

try:
  with open('token','r') as token_f:
    token = token_f.read().strip('\n')

except FileNotFoundError:
  if len(argv) < 2:
    print('Please remember you need to enter a token for the bot as an argument, or create a file called \'token\' and enter your token into it.')
  else:
    token = argv[1]

else:
  client.loop.create_task(event_dispatch())
  client.run(token)
