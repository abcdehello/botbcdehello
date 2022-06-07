import random
import math

import jsonprocessor as json
import discordio as io
import embedbuilder as builder
import gascoinprocess as gascoin
import cryptominer as miner

stanrate={'-50':5,'-20':10,'-10':15,'0':25,'10':20,'20':15,'50':5,'100':5}

async def stan(ctx,userid,count):
    userinfo=await json.read('userinfo.json')
    itemcnt=userinfo[userid]['inventory']['stan']
    if (itemcnt<count):
        await io.reply(ctx,'',await builder.buildDesc('Insufficient Amount','You do not own that many stans',0))
        return
    rewards={'-50':0,'-20':0,'-10':0,'0':0,'10':0,'20':0,'50':0,'100':0}
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
        await io.reply(ctx,'',await builder.buildDesc('Insufficient Amount','You do not own that many stans',0))
        return
    userinfo[userid]['inventory']['fries']-=count
    rewards={'0':0,'5':0,'10':0,'50':0,'100':0,'250':0,'1000':0,'vip':0}
    for i in range (count):
        seed=random.randint(0,999999)
        if (seed<500000):
            rewards['0']+=1
        elif (seed<800000):
            rewards['5']+=1
        elif (seed<950000):
            rewards['10']+=1
        elif (seed<980000):
            rewards['50']+=1
        elif (seed<990000):
            rewards['100']+=1
        elif (seed<999000):
            rewards['250']+=1
        elif (seed<999900):
            rewards['1000']+=1
        else:
            rewards['vip']+=1
    total=0
    desc=''
    for reward in rewards.keys():
        if (rewards[reward]>0):
            desc+=str(rewards[reward])+'x **'+reward+'** <:gascoin:981542532586569808>\n'
            if (reward!='vip'):
                total+=int(reward)*rewards[reward]
            else:
                if not (userinfo[userid]['isvip']):
                    userinfo[userid]['isvip']=True
                    rewards['vip']-=1
                total+=rewards['vip']*100000
    await gascoin.putmon(ctx,userid,total)
    await json.write('userinfo.json',userinfo)
    await io.reply(ctx,'',await builder.buildDesc('Loot from Fries',desc,1))