from token import MINEQUAL
import discordio as io
import embedbuilder as builder
import jsonprocessor as json
import gascoinprocess as gascoin
import math
import time

def buymultiplier(cnt):
    return math.pow((1.17+cnt/8.5),2.3)

def upgrademultiplier(lvl):
    return 0.23561*math.pow(lvl,1.352)+0.5

def harvestmultiplier(lvl):
    return 0.73*math.log(lvl)+0.26

async def listshop(ctx,userid):
    spec=await json.read('minespec.json')
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
    except KeyError:
        userinfo[userid]=[]
    fields=[]
    cnt=0
    for mine in spec.keys():
        cnt+=1
        field=[]
        field.append(mine+' '+spec[mine]['name']+' (Lv 1)')
        info='Produces '+str(math.floor(spec[mine]['rate']*harvestmultiplier(1)))+' '+spec[mine]['type']+'(s) per hour.\n'
        info+='Costs '+str(math.floor(spec[mine]['buycost']*buymultiplier(len(userinfo[userid]))))+' <:gascoin:981542532586569808>.\n'
        field.append(info)
        fields.append(field)
    await io.reply(ctx,'',await builder.buildField('Miner Shop',fields,1))

async def buymine(ctx,userid,mine):
    spec=await json.read('minespec.json')
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
    except KeyError:
        userinfo[userid]=[]
    if not (mine in spec.keys()):
      await io.reply(ctx,'',await builder.buildDesc('Invalid Mine','Please use `?cryptomine shop`',0))
      return
    money=await gascoin.getmon(userid)
    cost=math.floor(spec[mine]['buycost']*buymultiplier(len(userinfo[userid])))
    if (money<cost):
        await io.reply(ctx,'',await builder.buildDesc('Too Broke','Imagine don\'t have enough money L',0))
        return
    minedata={}
    minedata['model']=mine
    minedata['type']=spec[mine]['type']
    minedata['buyspent']=cost
    minedata['upgradespent']=0
    minedata['rate']=spec[mine]['rate']
    minedata['lastharvest']=time.time()
    minedata['level']=1
    userinfo[userid].append(minedata)
    await gascoin.putmon(ctx,userid,-cost)
    await json.write('userinfo.json',userinfo)
    await io.reply(ctx,'',await builder.buildDesc('Purchase Successful','You bought a new '+spec[mine]['name']+' (Lv 1)!',1))