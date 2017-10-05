from globalvars import client, current_players, games

async def show_players(message):
  if message.author in current_players:
    for lobby in games:
      if message.author in lobby.players:
        await client.send_message(message.channel,'\n- ' + '\n- '.join([p.mention for p in lobby.players]))

  else:
    await client.send_message(message.channel, 'You are not in a match! To join a match, use `hm>join`. To create a match, use `hm>create`')
