import jsonprocessor as json
import discordio as io
import embedbuilder as builder

async def listall(ctx):
    cmdjson=await json.read('help.json')
    cmdlst=''
    for category in cmdjson.keys():
      cmdlst+='`'+category+'`\n'
    await io.reply(ctx,'',await builder.buildDesc('Command Categories',cmdlst,1))

async def listsubcmd(ctx,cmd):
  cmdjson=await json.read('help.json')
  for category in cmdjson.keys():
    if (cmd.lower() in cmdjson[category].keys()):
      desc=''
      for subcmd in cmdjson[category][cmd]:
        desc+='**'+subcmd+'** :\n'+cmdjson[category][cmd][subcmd]+'\n'
      await io.reply(ctx,'',await builder.buildDesc('Sucommands of '+cmd,desc,1))
      return
  await listall(ctx)


async def listcmd(ctx,category):
    cmdjson=await json.read('help.json')
    desc=''
    for cmd in cmdjson[category.lower()].keys():
      desc+='`'+cmd+'`\n'
    await io.reply(ctx,'',await builder.buildDesc('Commands in the '+category+' Category',desc,1))