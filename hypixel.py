import requests
import discordio as io
import embedbuilder as builder
import os

apikey=os.getenv('hypixel_api_token')

async def getuuid(playername):
    response=requests.get('https://api.mojang.com/users/profiles/minecraft/'+playername).json()
    return response['id']

async def keyCheck(ctx):
    response=requests.get('https://api.hypixel.net/key?key='+apikey).json()
    if (response['success']):
        await io.reply(ctx,'',await builder.buildDesc('Bot Hypixel API Key Status','API key is valid with '+str(response['record']['limit']-response['record']['queriesInPastMin'])+' quotas left in this minute',1))
    else:
        await io.reply(ctx,'',await builder.buildDesc('Bot Hypixel API Key Status','API key is not valid',0))

async def statusCheck(ctx,playername):
    uuid=await getuuid(playername)
    response=requests.get('https://api.hypixel.net/status?uuid='+uuid+'&key='+apikey).json()
    print(response)
    if not (response['success']):
        await keyCheck(ctx)
        return
    if (response['session']['online']):
        playing=response['session']['gameType']+' - '+response['session']['mode']+' - '+response['session']['map']
        await io.reply(ctx,'',await builder.buildDesc('Online Status of '+playername,'**'+playername+'** is playing '+playing,1))
    else:
        await io.reply(ctx,'',await builder.buildDesc('Online Status of '+playername,'**'+playername+'** is not online',1))