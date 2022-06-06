import random
import math

import jsonprocessor as json
import discordio as io
import embedbuilder as builder
import gascoinprocess as gascoin
import cryptominer as miner

stanrate={"-50":5,"-20":10,"-10":15,"0":25,"10":20,"20":15,"50":5,"100":5}

async def suppository(ctx,userid,count):
    userinfo=await json.read('userinfo.json')
    itemcnt=userinfo[userid]['inventory']['suppository']
    if (itemcnt<count):
        await io.reply(ctx,'',await builder.buildDesc('Insufficient Amount','You do not own that many suppositories',0))
        return
    userinfo[userid]['inventory']['suppository']-=count
    total=0
    minecnt=0
    for i in range(count):
        total+=random.randint(10,25)
    for mine in userinfo[userid]['mines']:
        if (mine['type']!='suppository'):
            minecnt+=1
    for mine in userinfo[userid]['mines']:
        if (mine['type']!='suppository'):
            mine['lastharvest']-=total/minecnt
    await json.write('userinfo.json',userinfo)
    await io.reply(ctx,'',await builder.buildDesc('Suppository(s) Used','The suppository(s) made the miners high, producing `'+str(math.floor(total/minecnt))+'` seconds worth of products',1))


async def stan(ctx,userid,count):
    userinfo=await json.read('userinfo.json')
    itemcnt=userinfo[userid]['inventory']['stan']
    if (itemcnt<count):
        await io.reply(ctx,'',await builder.buildDesc('Insufficient Amount','You do not own that many stans',0))
        return
    rewards={"-50":0,"-20":0,"-10":0,"0":0,"10":0,"20":0,"50":0,"100":0}
    userinfo[userid]['inventory']['stan']-=count
    for i in range(count):
        percent=random.randint(0,99)
        for reward in stanrate.keys():
            if (percent<stanrate[reward]):
                rewards[reward]+=1
                break
            percent-=stanrate[reward]
    desc=''
    total=0
    for reward in rewards.keys():
        if (rewards[reward]>0):
            desc+=str(rewards[reward])+'x **'+reward+'** <:gascoin:981542532586569808>\n'
        total+=int(reward)*rewards[reward]
    await gascoin.putmon(ctx,userid,total)
    await json.write('userinfo.json',userinfo)
    await io.reply(ctx,'',await builder.buildDesc('Loot from Stans',desc,1))

async def fries(ctx,userid,count):
    userinfo=await json.read('userinfo.json')
    itemcnt=userinfo[userid]['inventory']['fries']
    if (itemcnt<count):
        await io.reply(ctx,'',await builder.buildDesc('Insufficient Amount','You do not own that many fries',0))
        return
    userinfo[userid]['inventory']['fries']-=count
    total=0
    for i in range(count):
        total+=random.randint(0,1)
    await json.write('userinfo.json',userinfo)
    await gascoin.putmon(ctx,userid,total)
    await io.reply(ctx,'',await builder.buildDesc('Fries Eaten','You feel very full after eating the fries, so you hankeyed on the road. EW!',1))