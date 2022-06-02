import requests
import discordio as io
import embedbuilder as builder

async def getuuid(playername):
    response=requests.get('https://api.mojang.com/users/profiles/minecraft/'+playername).json()
    return response['id']

async def namehistory(ctx,playername):
    uuid=await getuuid(playername)
    response=requests.get('https://api.mojang.com/user/profiles/'+uuid+'/names').json()
    desc=''
    for i in range(len(response)):
        desc+=str(i+1)+'. `'+response[i]['name']+'`'
        if (i>0):
            desc+=' Name changed to at: <t:'+str(round(response[i]['changedToAt']/1000))+':D>'
        desc+='\n'
    await io.reply(ctx,'',await builder.buildDesc('Name History of '+playername,desc,1,'https://crafatar.com/avatars/'+uuid+'?overlay'))

async def getskin(ctx,playername):
    uuid=await getuuid(playername)
    await io.reply(ctx,'',await builder.buildDesc('Skin of '+playername,'',1,'https://crafatar.com/renders/body/'+uuid+'?overlay',1))