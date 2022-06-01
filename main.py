import discord
from discord.ext import commands
import json
import os
import sys

import embedbuilder as builder
import discordio as io
import jsonprocessor as json
import cryptominer as miner
import minesweeper as mine

TOKEN=os.getenv('token')

bot = commands.Bot(command_prefix='&')
bot.remove_command('help')

@bot.event
async def on_ready():
  print('Bot Is Up!')

@bot.command(aliases=['h'])
async def help(ctx,*args):
  cmdjson=await json.read('help.json')
  if (len(args)==0):
    cmdlst=''
    for command in cmdjson.keys():
      cmdlst+='`'+command+'`\n'
    await io.reply(ctx,'',await builder.buildDesc('List Of Commands',cmdlst,1))
  elif (len(args)==1):
    cmd=str(args[0])
    if cmd in cmdjson.keys():
      subcmdlst=''
      for subcommand in cmdjson[cmd].keys():
        subcmdlst+='**'+subcommand+'**: '+cmdjson[cmd][subcommand]+'\n'
      await io.reply(ctx,'',await builder.buildDesc('Subcommands Of Command '+cmd,subcmdlst,1))
    else:
      await io.reply(ctx,'',await builder.buildDesc('Command Not Found','Please use `?help`',0))
  else:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `?help`',0))

@bot.command(aliases=['ms'])
async def minesweeper(ctx,*args):
  try:
    action=str(args[0])
  except:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `?help`',0))
    return
  if (action=='new'):
    try:
      diff=str(args[1])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `?help`',0))
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
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `?help`',0))
  elif (action=='print'):
    await mine.printBoard(ctx,str(ctx.author.id))
  elif (action=='open'):
    try:
      x=int(args[1])
      y=int(args[2])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `?help`',0))
      return
    if (await mine.openCell(ctx,str(ctx.author.id),x,y)):
      await mine.printBoard(ctx,str(ctx.author.id))
  elif (action=='flag'):
    try:
      x=int(args[1])
      y=int(args[2])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `?help`',0))
      return
    if (await mine.flagCell(ctx,str(ctx.author.id),x,y)):
      await mine.printBoard(ctx,str(ctx.author.id))
  elif (action=='unflag'):
    try:
      x=int(args[1])
      y=int(args[2])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `?help`',0))
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
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `?help`',0))

@bot.command(aliases=['cm'])
async def cryptomine(ctx,*args):
  try:
    action=str(args[0])
  except:
    await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `?help`',0))
    return
  if (action=='shop'):
    await miner.listshop(ctx,str(ctx.author.id))
  elif (action=='buy'):
    try:
      mine=str(args[1])
    except:
      await io.reply(ctx,'',await builder.buildDesc('Invalid Arguments','Please use `?help`',0))
      return
    await miner.buymine(ctx,str(ctx.author.id),mine)

bot.run(TOKEN)