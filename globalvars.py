import discord


client = discord.Client()

games = []
current_players = []
active_channels = []

alphabet = 'abcdefghijklmnopqrstuvwxyz '

def alphaStr(string):
  string = str(string)
  for char in string:
    if char in alphabet:
      continue
    else:
      return False
  return True
