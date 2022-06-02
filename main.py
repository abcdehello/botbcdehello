import asyncio
import discord
from discord.ext import commands
import os

import embedbuilder as builder
import discordio as io
import jsonprocessor as json


import cryptominer as miner
import help as listhelp
import minecraftinfo as mcinfo
import minesweeper as mine
import wikipedia as wiki

TOKEN=os.getenv('token')

bot=commands.Bot(command_prefix='&',intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
  await bot.wait_until_ready()
  print('Bot Is Up!')

@bot.event
async def on_message(msg):
  await bot.process_commands(msg)

@bot.command(aliases=['h'])
async def help(ctx,*args):
  try:
    name=str(args[0])
  except:
    await listhelp.listall(ctx)
    return
  cmdjson=await json.read('help.json')
  if (name in cmdjson.keys()):
    await listhelp.listcmd(ctx,name)
    return
  else:
    await listhelp.listsubcmd(ctx,name)
@bot.command(aliases=['sp'])
async def spam(ctx,*args):
  try:
    cnt=int(args[-1])
    msg=''
    for i in range(len(args)-1):
      if (i>0):
        msg+=' '
      msg+=str(args[i])
  except:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))
  hasping=False
  if hasping:
    await io.reply(ctx,'',await builder.buildDesc('Command Blocked','Ping detected',0))
    return
  for i in range(cnt):
    await io.send(ctx,msg,None)
    await asyncio.sleep(0.75)

@bot.command()
async def userinfo(ctx,*args):
  try:
    action=str(args[0])
  except:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))
    return
  if (action=='namehistory') or (action=='namehis'):
    try:
      username=str(args[1])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))
      return
    await mcinfo.namehistory(ctx,username)
  elif (action=='skin'):
    try:
      username=str(args[1])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))
      return
    await mcinfo.getskin(ctx,username)

@bot.command(aliases=['wiki'])
async def wikipedia(ctx,*args):
  title=''
  for i in range(len(args)):
    if (i>0):
      title+=' '
    title+=str(args[i])
  if (title==''):
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))
    return
  await wiki.search(ctx,title)
  

@bot.command(aliases=['ms'])
async def minesweeper(ctx,*args):
  try:
    action=str(args[0])
  except:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))
    return
  if (action=='new'):
    try:
      diff=str(args[1])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))
      return
    if (diff=='easy'):
      await mine.makeBoard(str(ctx.author.id),5,4)
      await mine.printBoard(ctx,str(ctx.author.id))
    elif (diff=='medium'):
      await mine.makeBoard(str(ctx.author.id),8,12)
      await mine.printBoard(ctx,str(ctx.author.id))
    elif (diff=='hard'):
      await mine.makeBoard(str(ctx.author.id),10,23)
      await mine.printBoard(ctx,str(ctx.author.id))
    elif (diff=='extreme'):
      await mine.makeBoard(str(ctx.author.id),14,36)
      await mine.printBoard(ctx,str(ctx.author.id))
    else:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))
  elif (action=='print'):
    await mine.printBoard(ctx,str(ctx.author.id))
  elif (action=='open'):
    try:
      x=int(args[1])
      y=int(args[2])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))
      return
    if (await mine.openCell(ctx,str(ctx.author.id),x,y)):
      await mine.printBoard(ctx,str(ctx.author.id))
  elif (action=='flag'):
    try:
      x=int(args[1])
      y=int(args[2])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))
      return
    if (await mine.flagCell(ctx,str(ctx.author.id),x,y)):
      await mine.printBoard(ctx,str(ctx.author.id))
  elif (action=='unflag'):
    try:
      x=int(args[1])
      y=int(args[2])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))
      return
    if (await mine.unflagCell(ctx,str(ctx.author.id),x,y)):
      await mine.printBoard(ctx,str(ctx.author.id))
  elif (action=='difficulty'):
    desc=''
    desc+='Easy: 5x5 board, 4 mines.\n'
    desc+='Medium: 8x8 board, 12 mines.\n'
    desc+='Hard: 10x10 board, 23 mines.\n'
    desc+='Extreme: 14x14 board, 36 mines.\n'
    await io.reply(ctx,'',await builder.buildDesc('Minesweeper Difficulty',desc,1))
  else:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))

@bot.command(aliases=['cm'])
async def cryptomine(ctx,*args):
  try:
    action=str(args[0])
  except:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))
    return
  if (action=='shop'):
    await miner.listshop(ctx,str(ctx.author.id))
  elif (action=='buy'):
    try:
      mine=str(args[1])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `&help`',0))
      return
    await miner.buymine(ctx,str(ctx.author.id),mine)

bot.run(TOKEN)