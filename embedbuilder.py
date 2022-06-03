import discord

url='https://bit.ly/3wtEnxo'

async def buildDesc(title,description,color,image=None,size=0):
  embed=discord.Embed()
  embed.url=url
  if (size==0):
    embed.set_thumbnail(url=image)
  else:
    embed.set_image(url=image)
  embed.title=title
  embed.description=description
  if (color==0):
    embed.color=discord.Color.red()
  elif (color==1):
   embed.color=discord.Color.green()
  elif (color==2):
    embed.color=discord.Color.yellow()
  return embed

async def buildField(title,fields,color):
  embed=discord.Embed()
  embed.url=url
  embed.title=title
  embed.description=''
  for field in fields:
    embed.add_field(name=field[0],value=str(field[1]),inline=True)
  if (color==0):
    embed.color=discord.Color.red()
  elif (color==1):
    embed.color=discord.Color.green()
  elif (color==2):
    embed.color=discord.Color.yellow()
  return embed