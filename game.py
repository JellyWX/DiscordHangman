import asyncio
import discord

from random import choice

from globalvars import *


class GameRoom(object):

  name = None
  public = 1
  password = ''
  max_players = 2

  closed = 0
  started = 0

  word = ''

  def __init__(self,channel):
    self.channel = channel
    active_channels.append(channel)
    self.players = []

  async def update_vars(self):
    self.name = str(self.name)
    self.password = str(self.password)
    self.max_players = int(self.max_players)

    if self.max_players <= 0:
      self.max_players = 4

    self.public = 1 if self.password == '' else 0

  async def join(self,user):
    print(self.players)
    if self.max_players > len(self.players) and user not in self.players:
      self.players.append(user)
      current_players.append(user)

    else:
      await client.send_message(user,'This lobby is full. Sorry kiddo')

  async def set_word(self):
    user_set = choice(self.players) ## select a user from the players on the game
    await client.send_message(user_set, '**It\'s your turn to choose a word!** Please type it below and hit enter:')

    wordm = await client.wait_for_message(author=user_set)
    word = wordm.content.lower()
    while not alphaStr(word):

      await client.send_message(user_set, 'Your word must consist only of English letters.')
      wordm = await client.wait_for_message(author=user_set)
      word = wordm.content.lower()

    self.word = word
    await client.send_message(user_set, 'Your word has been set to {}!'.format(word))


  async def process_guess(self,guess):
    if len(guess) > 1:
      pass

  async def quit(self,user):
    await client.send_message(self.channel,'Boo! {} pussied out. What a loser.'.format(user.name))
    self.players.remove(user)
