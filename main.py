import asyncio
import discord
from discord.ext import commands
import os
import time

import embedbuilder as builder
import discordio as io
import jsonprocessor as json


import cryptominer as miner
import help as listhelp
import hypixel as hyp
import minecraftinfo as mcinfo
import minesweeper as mine
import wikipedia as wiki
import mute as mu

TOKEN=os.getenv('token')
OWNER=os.getenv('owner_id')
PREFIX=os.getenv('prefix')

bot=commands.Bot(command_prefix=PREFIX,intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
  await bot.wait_until_ready()
  print('Bot Is Up!')

@bot.event
async def on_message(msg):
  muted=await json.read('muted.json')
  if not (msg.content.startswith(PREFIX)):
    return
  try:
    untilunmute=muted[str(msg.author.id)]
    if (untilunmute>=time.time()):
      await io.reply(msg,'',await builder.buildDesc('Muted','You are muted until <t:'+str(untilunmute)+':f>',2))
      return
  except:
    dummy=0
  await bot.process_commands(msg)
  

@bot.event
async def on_command_error(ctx,error):
  if isinstance(error,commands.CommandNotFound):
    await io.reply(ctx,'',await builder.buildDesc('Command Not Found','Please use `^help`',0))

#Admin Commands

@bot.command(aliases=['kill','stop'])
async def halt(ctx):
  if (str(ctx.author.id)!=OWNER):
    await io.reply(ctx,'',await builder.buildDesc('Insufficient Permission','You cannot execute this command',0))
    return
  await io.send(ctx,'',await builder.buildDesc('Command Received','Bot stopping...',1))
  exit()

@bot.command()
async def mute(ctx,*args):
  if (str(ctx.author.id)!=OWNER):
    await io.reply(ctx,'',await builder.buildDesc('Insufficient Permission','You cannot execute this command',0))
    return
  try:
    user=int(args[0])
    dura=int(args[1])
  except:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
    return
  await mu.mute(ctx,str(user),dura)

#Help Commands

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

#Misc Commands

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
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
    return
  hasping=False
  if hasping:
    await io.reply(ctx,'',await builder.buildDesc('Command Blocked','Ping detected',0))
    return
  for i in range(cnt):
    await io.send(ctx,msg,None)
    await asyncio.sleep(0.75)

#Search Commands

@bot.command()
async def userinfo(ctx,*args):
  try:
    action=str(args[0])
  except:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
    return
  if (action=='namehistory') or (action=='namehis'):
    try:
      username=str(args[1])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
      return
    await mcinfo.namehistory(ctx,username)
  elif (action=='skin'):
    try:
      username=str(args[1])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
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
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
    return
  await wiki.search(ctx,title)

@bot.command(aliases=['hy'])
async def hypixel(ctx,*args):
  try:
    action=str(args[0])
  except:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
    return
  if (action=='keycheck'):
    await hyp.keyCheck(ctx)
  elif (action=='status'):
    try:
      username=str(args[1])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
      return
    await hyp.statusCheck(ctx,username)
  
#Game Commands

@bot.command(aliases=['ms'])
async def minesweeper(ctx,*args):
  try:
    action=str(args[0])
  except:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
    return
  if (action=='new'):
    try:
      diff=str(args[1])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
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
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
  elif (action=='print'):
    await mine.printBoard(ctx,str(ctx.author.id))
  elif (action=='open'):
    try:
      x=int(args[1])
      y=int(args[2])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
      return
    if (await mine.openCell(ctx,str(ctx.author.id),x,y)):
      await mine.printBoard(ctx,str(ctx.author.id))
  elif (action=='flag'):
    try:
      x=int(args[1])
      y=int(args[2])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
      return
    if (await mine.flagCell(ctx,str(ctx.author.id),x,y)):
      await mine.printBoard(ctx,str(ctx.author.id))
  elif (action=='unflag'):
    try:
      x=int(args[1])
      y=int(args[2])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
      return
    if (await mine.unflagCell(ctx,str(ctx.author.id),x,y)):
      await mine.printBoard(ctx,str(ctx.author.id))
  elif (action=='difficulty') or (action=='diff'):
    await mine.listdiff(ctx)
  else:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))

@bot.command(aliases=['cm'])
async def cryptomine(ctx,*args):
  try:
    action=str(args[0])
  except:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
    return
  if (action=='new'):
    await miner.createprofile(ctx,str(ctx.author.id))
  elif (action=='mineshop') or (action=='ms'):
    await miner.listmineshop(ctx,str(ctx.author.id))
  elif (action=='itemshop') or (action=='is'):
    await miner.listitemshop(ctx)
  elif (action=='buy'):
    try:
      mine=str(args[1])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
      return
    await miner.buymine(ctx,str(ctx.author.id),mine)
  elif (action=='listmine') or (action=='lm'):
    await miner.listmine(ctx,str(ctx.author.id))
  elif (action=='sellmine') or (action=='sm'):
    try:
      id=int(args[1])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
      return
    if (id<1):
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
      return
    await miner.sellmine(ctx,str(ctx.author.id),id)
  elif (action=='harvest'):
    await miner.harvestmine(ctx,str(ctx.author.id))
  elif (action=='inventory') or (action=='listinv'):
    await miner.listinv(ctx,str(ctx.author.id))
  elif (action=='sellitem'):
    try:
      item=str(args[1])
      count=int(args[2])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
      return
    if (count<1):
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
      return
    await miner.sellitem(ctx,str(ctx.author.id),item,count)
  elif (action=='upgrade') or (action=='up'):
    try:
      id=int(args[1])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
      return
    if (id<1):
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))
      return
    await miner.upgrademine(ctx,str(ctx.author.id),id)
  else:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `^help`',0))

bot.run(TOKEN)