import asyncio
import discord

from random import choice

from globalvars import *


class GameRoom(object):

  name = None
  public = 1
  password = ''
  max_players = 6

  closed = 0
  started = 0

  word = ''

  guesses = 10

  used_guesses = 0

  def __init__(self,channel):
    self.channel = channel
    active_channels.append(channel)
    self.players = []
    self.active_player = None
    self.output_str = []

  async def update_vars(self):
    self.name = str(self.name)
    self.password = str(self.password)
    self.max_players = int(self.max_players)

    if self.max_players <= 0:
      self.max_players = 4

    self.public = 1 if self.password == '' else 0

  async def join(self,user):
    if self.max_players < len(self.players):
      await client.send_message(user,'This lobby is full. Sorry kiddo')

    else:
      self.players.append(user)
      current_players.append(user)

  async def set_word(self):
    print('match has begun. selecting player')
    user_set = choice(self.players) ## select a user from the players on the game

    print('player {} selected. DMing now'.format(user_set.name))
    await client.send_message(self.channel, '{} has been chosen to select a word! (check your DMs {})'.format(user_set.name, user_set.mention))
    e = await client.send_message(user_set, '**It\'s your turn to choose a word!** Please type it below and hit enter:')

    wordm = await client.wait_for_message(author=user_set,channel=e.channel)

    print(wordm.channel)
    print(e.channel)

    word = wordm.content.lower()
    while not alphaStr(word):

      await client.send_message(user_set, 'Your word must consist only of English letters.')
      wordm = await client.wait_for_message(author=user_set)
      word = wordm.content.lower()

    self.output_str = []

    self.word = word
    for char in self.word:
      if char == ' ':
        self.output_str.append('/')
      else:
        self.output_str.append('-')

    await client.send_message(user_set, 'Your word has been set to {}!'.format(word))
    await client.send_message(self.channel, '{} has finished setting the word; start guessing (a guess starts with a `?` character)!\n{}'.format(user_set.name,''.join(self.output_str)))

    self.active_player = user_set

  async def process_guess(self,guess):
    if len(guess) > 1 and guess != self.word:
      await client.send_message(self.channel, 'Incorrect! The word was {}. Better luck next time! Type `hm>start` to restart'.format(self.word))
      self.word = ''
      self.started = 0

    elif guess == self.word:
      await client.send_message(self.channel, 'Correct! The word was {}! Type `hm>start` to restart'.format(self.word))
      self.word = ''
      self.started = 0

    else:
      if guess in self.word:

        x = 0
        for char in self.word:
          if char == guess:
            self.output_str[x] = guess
          x += 1

        if '-' not in self.output_str:
          await client.send_message(self.channel, 'You got it! The word was {}! Type `hm>start` to restart'.format(self.word))
          self.word = ''
          self.started = 0

          return

        await client.send_message(self.channel, 'You guessed one character correctly.\n{}'.format(''.join(self.output_str)))

      else:
        self.used_guesses += 1
        await client.send_message(self.channel, 'Incorrect guess! Try again ({} incorrect guesses remaining)\n{}'.format(self.guesses-self.used_guesses,''.join(self.output_str)))

        if self.used_guesses >= self.guesses:
          await client.send_message(self.channel, 'You ran out of guesses! The word was {}. Better luck next time! Type `hm>start` to restart'.format(self.word))
          self.word = ''
          self.started = 0

  async def quit(self,user):
    await client.send_message(self.channel,'Boo! {} pussied out. What a loser.'.format(user.name))
    self.players.remove(user)
