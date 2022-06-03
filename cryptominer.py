from distutils.command.build import build
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

async def createprofile(ctx,userid):
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
        await io.reply(ctx,'',await builder.buildDesc('Profile Already Exist','You already have a profile',0))
    except KeyError:
        userinfo[userid]={}
        userinfo[userid]['mines']=[]
        userinfo[userid]['inventory']={}
        await json.write('userinfo.json',userinfo)
        await io.reply(ctx,'',await builder.buildDesc('Profile Created','You now have a profile',1))

async def listmineshop(ctx,userid):
    spec=await json.read('minespec.json')
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
    except KeyError:
        await io.reply(ctx,'',await builder.buildDesc('Profile Do Not Exist','You don\'t have a profile',0))
        return
    fields=[]
    cnt=0
    for mine in spec.keys():
        cnt+=1
        field=[]
        field.append(mine+' '+spec[mine]['name']+' (Lv 1)')
        info='Produces '+str(math.floor(spec[mine]['rate']*harvestmultiplier(1)))+' '+spec[mine]['type']+'(s) per hour.\n'
        info+='Costs '+str(math.floor(spec[mine]['buycost']*buymultiplier(len(userinfo[userid]['mines']))))+' <:gascoin:981542532586569808>.\n'
        field.append(info)
        fields.append(field)
    await io.reply(ctx,'',await builder.buildField('Miner Shop',fields,1))

async def buymine(ctx,userid,mine):
    spec=await json.read('minespec.json')
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
    except KeyError:
        await io.reply(ctx,'',await builder.buildDesc('Profile Do Not Exist','You don\'t have a profile',0))
        return
    if not (mine in spec.keys()):
      await io.reply(ctx,'',await builder.buildDesc('Invalid Mine','Please use `&cryptomine mineshop`',0))
      return
    money=await gascoin.getmon(userid)
    cost=math.floor(spec[mine]['buycost']*buymultiplier(len(userinfo[userid]['mines'])))
    if (money<cost):
        await io.reply(ctx,'',await builder.buildDesc('Too Broke','Imagine don\'t have enough money L',0))
        return
    minedata={}
    minedata['model']=mine
    minedata['type']=spec[mine]['type']
    minedata['buyspent']=cost
    minedata['upgradespent']=0
    minedata['rate']=spec[mine]['rate']
    minedata['upgradecost']=spec[mine]['upgradecost']
    minedata['lastharvest']=time.time()
    minedata['level']=1
    userinfo[userid]['mines'].append(minedata)
    await gascoin.putmon(ctx,userid,-cost)
    await io.reply(ctx,'',await builder.buildDesc('Purchase Successful','You bought a new '+spec[mine]['name']+' (Lv 1)!',1))
    await json.write('userinfo.json',userinfo)

async def sellmine(ctx,userid,mineid):
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
    except KeyError:
        await io.reply(ctx,'',await builder.buildDesc('Profile Do Not Exist','You don\'t have a profile',0))
        return
    if (mineid>len(userinfo[userid]['mines'])):
        await io.reply(ctx,'',await builder.buildDesc('Invalid ID','You do not own that many mines',0))
        return
    mineid-=1
    usermines=[]
    sellmine={}
    sellprice=math.floor((userinfo[userid]['mines'][mineid]['buyspent']+userinfo[userid]['mines'][mineid]['upgradespent'])*0.9)
    for i in range (len(userinfo[userid]['mines'])):
        if (i!=mineid):
            usermines.append(userinfo[userid]['mines'][i])
        else:
            sellmine=userinfo[userid]['mines'][i]
    await gascoin.putmon(ctx,userid,sellprice)
    userinfo[userid]['mines']=usermines
    await io.reply(ctx,'',await builder.buildDesc('Sell Successful','You sold your (Lv '+str(sellmine['level'])+') '+sellmine['model'],1))
    await json.write('userinfo.json',userinfo)

async def listmine(ctx,userid):
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
    except KeyError:
        await io.reply(ctx,'',await builder.buildDesc('Profile Do Not Exist','You don\'t have a profile',0))
        return
    if (len(userinfo[userid]['mines'])==0):
        await io.reply(ctx,'',await builder.buildDesc('You Do Not Own Any Mines','Please use `&cryptomine buy`',0))
        return
    cnt=0
    mines=[]
    for mine in userinfo[userid]['mines']:
        cnt+=1
        title=str(cnt)+'. '+mine['model']+' (Lv '+str(mine['level'])+')'
        desc='Costs '+str(math.floor(mine['upgradecost']*upgrademultiplier(mine['level'])))+' <:gascoin:981542532586569808> to upgrade.'
        mines.append([title,desc])
    await io.reply(ctx,'',await builder.buildField('Your Mines',mines,1))

async def upgrademine(ctx,userid,mineid):
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
    except KeyError:
        await io.reply(ctx,'',await builder.buildDesc('Profile Do Not Exist','You don\'t have a profile',0))
        return
    if (mineid>len(userinfo[userid]['mines'])):
        await io.reply(ctx,'',await builder.buildDesc('Invalid ID','You do not own that many mines',0))
        return
    mineid-=1
    money=await gascoin.getmon(userid)
    cost=math.floor(userinfo[userid]['mines'][mineid]['upgradecost']*upgrademultiplier(userinfo[userid]['mines'][mineid]['level']))
    if (money<cost):
        await io.reply(ctx,'',await builder.buildDesc('Too Broke','Imagine don\'t have enough money L',0))
        return
    userinfo[userid]['mines'][mineid]['level']+=1
    userinfo[userid]['mines'][mineid]['upgradespent']+=cost
    await gascoin.putmon(ctx,userid,-cost)
    await io.reply(ctx,'',await builder.buildDesc('Upgrade Successful','Your '+userinfo[userid]['mines'][mineid]['model']+' has been upgraded to Lv '+str(userinfo[userid]['mines'][mineid]['level'])+'!',1))
    await json.write('userinfo.json',userinfo)
    

async def harvestmine(ctx,userid):
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
    except KeyError:
        await io.reply(ctx,'',await builder.buildDesc('Profile Do Not Exist','You don\'t have a profile',0))
        return
    reward={}
    if (len(userinfo[userid]['mines'])==0):
        await io.reply(ctx,'',await builder.buildDesc('You Do Not Own Any Mines','Please use `&cryptomine buy`',0))
        return
    for mine in userinfo[userid]['mines']:
        rph=math.floor(mine['rate']*harvestmultiplier(mine['level']))
        hrs=math.floor((time.time()-mine['lastharvest'])/3600)
        mine['lastharvest']+=hrs*3600
        try:
            dummy=userinfo[userid]['inventory'][mine['type']]
        except KeyError:
            userinfo[userid]['inventory'][mine['type']]=0
        if (mine['type']!='gascoin'):
            userinfo[userid]['inventory'][mine['type']]+=rph*hrs
        try:
            dummy=reward[mine['type']]
        except KeyError:
            reward[mine['type']]=0
        reward[mine['type']]+=rph*hrs
    try:
        await gascoin.putmon(reward['gascoin'])
    except:
        dummy
    desc=''
    for item in reward.keys():
        desc+='`'+str(reward[item])+'x` **'+item+'**\n'
    await io.reply(ctx,'',await builder.buildDesc('Harvested Items',desc,1))
    await json.write('userinfo.json',userinfo)

async def listinv(ctx,userid):
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
    except KeyError:
        await io.reply(ctx,'',await builder.buildDesc('Profile Do Not Exist','You don\'t have a profile',0))
        return
    items=list(userinfo[userid]['inventory'].keys())
    desc=''
    for item in items:
        desc+='`'+str(userinfo[userid]['inventory'][item])+'x` **'+item+'**\n'
    await io.reply(ctx,'',await builder.buildDesc('Your Inventory',desc,1))

async def listitemshop(ctx):
    prices=await json.read('itemprice.json')
    items=[]
    for item in prices.keys():
        items.append([prices[item],item])
    items.sort()
    items.reverse()
    desc=''
    for item in items:
        desc+='**'+item[1]+'** : '+str(item[0])+'<:gascoin:981542532586569808>\n'
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
        await io.reply(ctx,'',await builder.buildDesc('Invalid Item','Please use `&cryptomine itemshop`',0))
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