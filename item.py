import jsonprocessor as json
import discordio as io
import embedbuilder as builder
import gascoinprocess as gascoin
import useitem as use

import asyncio
import math
import time

async def listinv(ctx,userid):
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
    except KeyError:
        await io.reply(ctx,'',await builder.buildDesc('Profile Do Not Exist','You don\'t have a profile',0))
        return
    items=list(userinfo[userid]['inventory'].keys())
    items.sort()
    desc=''
    for item in items:
        if (userinfo[userid]['inventory'][item]>0):
            desc+='`'+str(userinfo[userid]['inventory'][item])+'x` **'+item+'**\n'
    await io.reply(ctx,'',await builder.buildDesc('Your Inventory',desc,1))

async def listshop(ctx):
    prices=await json.read('itemprice.json')
    items=[]
    for item in prices.keys():
        items.append([prices[item],item])
    items.sort()
    items.reverse()
    desc=''
    for item in items:
        desc+='Sell price of **'+item[1]+'** : '+str(item[0])+'<:gascoin:981542532586569808>\n'
    await io.reply(ctx,'',await builder.buildDesc('Item Prices',desc,1))

async def sellitem(ctx,userid,item,count):
    prices=await json.read('itemprice.json')
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
    except KeyError:
        await io.reply(ctx,'',await builder.buildDesc('Profile Do Not Exist','You don\'t have a profile',0))
        return
    if not (item in prices.keys()):
        await io.reply(ctx,'',await builder.buildDesc('Invalid Item','Please use `^cryptomine itemshop`',0))
        return
    try:
        dummy=userinfo[userid]['inventory'][item]
    except KeyError:
        await io.reply(ctx,'',await builder.buildDesc('Insufficient Amount','You don\'t own that many '+item+'(s)',0))
        return
    if (count>userinfo[userid]['inventory'][item]):
        await io.reply(ctx,'',await builder.buildDesc('Insufficient Amount','You don\'t own that many '+item+'(s)',0))
        return
    userinfo[userid]['inventory'][item]-=count
    await gascoin.putmon(ctx,userid,prices[item]*count)
    await json.write('userinfo.json',userinfo)

async def useitem(ctx,userid,item,count):
    userinfo=await json.read('userinfo.json')
    try:
        nextuse=userinfo[userid]['lastitemuse']+10
        if (nextuse>time.time()):
            await io.reply(ctx,'',await builder.buildDesc('Item Usage on Cooldown','Please wait '+str(math.ceil(nextuse-time.time()))+' more seconds before using an item',2))
            return
    except:
        userinfo[userid]['lastitemuse']=time.time()
    try:
        dummy=userinfo[userid]['inventory'][item]
    except:
        await io.reply(ctx,'',await builder.buildDesc('Invalid Item','This item does not exist or you do not own any of it',0))
        return
    if (item=='stan'):
        userinfo[userid]['lastitemuse']=time.time()
        await json.write('userinfo.json',userinfo)
        await asyncio.sleep(1)
        await use.stan(ctx,userid,count)
    elif (item=='fries'):
        userinfo[userid]['lastitemuse']=time.time()
        await json.write('userinfo.json',userinfo)
        await asyncio.sleep(1)
        await use.fries(ctx,userid,count)
    else:
        await io.reply(ctx,'',await builder.buildDesc('Invalid Item','This item does not exist or cannot be used',0))