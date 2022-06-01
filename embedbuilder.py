import discord

async def buildDesc(title,description,color):
  embed=discord.Embed()
  embed.title=title
  embed.description=description
  if (color==0):
    embed.color=discord.Color.red()
  elif (color==1):
   embed.color=discord.Color.green()
  return embed

async def buildField(title,fields,color):
  embed=discord.Embed()
  embed.title=title
  embed.description=''
  for field in fields:
    embed.add_field(name=field[0],value=str(field[1]),inline=True)
  if (color==0):
    embed.color=discord.Color.red()
  elif (color==1):
    embed.color=discord.Color.green()
  return embed