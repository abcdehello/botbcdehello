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
    return 2.73*math.log(lvl)+1.26

async def createprofile(ctx,userid):
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
        await io.reply(ctx,'',await builder.buildDesc('Profile Already Exist','You already have a profile',0))
    except KeyError:
        userinfo[userid]={}
        userinfo[userid]['mines']=[]
        userinfo[userid]['inventory']={}
        userinfo[userid]['isvip']=False
        await json.write('userinfo.json',userinfo)
        await io.reply(ctx,'',await builder.buildDesc('Profile Created','You now have a profile',1))

async def listshop(ctx,userid):
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
      await io.reply(ctx,'',await builder.buildDesc('Invalid Mine','Please use `^cryptomine shop`',0))
      return
    if (not (userinfo[userid]['isvip'])) and (len(userinfo[userid]['mines'])==10):
        await io.reply(ctx,'',await builder.buildDesc('Mine Slots Full','Please sell some of your mines or get VIP',0))
        return
    elif (userinfo[userid]['isvip']) and (len(userinfo[userid]['mines'])==20):
        await io.reply(ctx,'',await builder.buildDesc('Mine Slots Full','Please sell some of your mines',0))
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
    await json.write('userinfo.json',userinfo)
    await io.reply(ctx,'',await builder.buildDesc('Purchase Successful','You bought a new '+spec[mine]['name']+' (Lv 1)!',1))

async def sellmine(ctx,userid,mineid):
    userinfo=await json.read('userinfo.json')
    sellprice=await json.read('itemprice.json')
    try:
        dummy=userinfo[userid]
    except KeyError:
        await io.reply(ctx,'',await builder.buildDesc('Profile Do Not Exist','You don\'t have a profile',0))
        return
    if (mineid>len(userinfo[userid]['mines'])):
        await io.reply(ctx,'',await builder.buildDesc('Invalid ID','You do not own that many mines',0))
        return
    mineid-=1
    mine=userinfo[userid]['mines'][mineid]
    usermines=[]
    sellmine={}
    sellprice=math.floor((mine['buyspent']+mine['upgradespent']*sellprice[mine['type']])*0.9)
    for i in range (len(userinfo[userid]['mines'])):
        if (i!=mineid):
            usermines.append(userinfo[userid]['mines'][i])
        else:
            sellmine=userinfo[userid]['mines'][i]
    await gascoin.putmon(ctx,userid,sellprice)
    userinfo[userid]['mines']=usermines
    await json.write('userinfo.json',userinfo)
    await io.reply(ctx,'',await builder.buildDesc('Sell Successful','You sold your (Lv '+str(sellmine['level'])+') '+sellmine['model'],1))

async def listmine(ctx,userid):
    userinfo=await json.read('userinfo.json')
    sellprice=await json.read('itemprice.json')
    sellprice['gascoin']=1
    try:
        dummy=userinfo[userid]
    except KeyError:
        await io.reply(ctx,'',await builder.buildDesc('Profile Do Not Exist','You don\'t have a profile',0))
        return
    if (len(userinfo[userid]['mines'])==0):
        await io.reply(ctx,'',await builder.buildDesc('You Do Not Own Any Mines','Please use `^cryptomine buy`',0))
        return
    cnt=0
    mines=[]
    for mine in userinfo[userid]['mines']:
        cnt+=1
        title=str(cnt)+'. '+mine['model']+' (Lv '+str(mine['level'])+')'
        rph=math.floor(mine['rate']*harvestmultiplier(mine['level']))
        desc=''
        desc+='Costs '+str(math.floor(mine['upgradecost']*upgrademultiplier(mine['level'])))+' '+mine['type']+'(s) to upgrade.\n'
        desc+='Generates '+str(math.floor(rph))+' item(s) per hour.\n'
        desc+='Can be sold for '+str(math.floor((mine['buyspent']+mine['upgradespent']*sellprice[mine['type']])*0.9))+' <:gascoin:981542532586569808>.'
        mines.append([title,desc])
    await io.reply(ctx,'',await builder.buildField('Your Mines',mines,1))

async def upgrademine(ctx,userid,mineid,level):
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
    total=0
    for i in range(level):
        mine=userinfo[userid]['mines'][mineid]
        if (mine['type']=='gascoin'):
            mat=await gascoin.getmon(userid)
        else:
            try:
                mat=userinfo[userid]['inventory'][mine['type']]
            except:
                mat=0
        cost=math.floor(mine['upgradecost']*upgrademultiplier(mine['level']))
        if (mat<cost):
            if (i==0):
                await io.reply(ctx,'',await builder.buildDesc('Too Broke','Imagine don\'t have enough material(s)/money L',0))
                return
            else:
                await io.reply(ctx,'',await builder.buildDesc('Upgrade Successful','Your '+userinfo[userid]['mines'][mineid]['model']+' has been upgraded to Lv '+str(userinfo[userid]['mines'][mineid]['level'])+'!',1))
                if (mine['type']!='gascoin'):
                    userinfo[userid]['inventory'][mine['type']]-=total
                else:
                    await gascoin.putmon(ctx,userid,-total)
                await json.write('userinfo.json',userinfo)
                return
        total+=cost
        userinfo[userid]['mines'][mineid]['level']+=1
        userinfo[userid]['mines'][mineid]['upgradespent']+=cost
    if (mine['type']!='gascoin'):
        userinfo[userid]['inventory'][mine['type']]-=total
    else:
        await gascoin.putmon(ctx,userid,-total)
    await json.write('userinfo.json',userinfo)
    await io.reply(ctx,'',await builder.buildDesc('Upgrade Successful','Your '+userinfo[userid]['mines'][mineid]['model']+' has been upgraded to Lv '+str(userinfo[userid]['mines'][mineid]['level'])+'!',1))
    

async def harvestmine(ctx,userid):
    userinfo=await json.read('userinfo.json')
    try:
        dummy=userinfo[userid]
    except KeyError:
        await io.reply(ctx,'',await builder.buildDesc('Profile Do Not Exist','You don\'t have a profile',0))
        return
    reward={}
    hascoin=False
    if (len(userinfo[userid]['mines'])==0):
        await io.reply(ctx,'',await builder.buildDesc('You Do Not Own Any Mines','Please use `^cryptomine buy`',0))
        return
    for mine in userinfo[userid]['mines']:
        rph=math.floor(mine['rate']*harvestmultiplier(mine['level']))
        hrs=(time.time()-mine['lastharvest'])/3600
        mine['lastharvest']=time.time()
        try:
            dummy=userinfo[userid]['inventory'][mine['type']]
        except KeyError:
            if (mine['type']!='gascoin'):
                userinfo[userid]['inventory'][mine['type']]=0
        if (mine['type']!='gascoin'):
            userinfo[userid]['inventory'][mine['type']]+=math.floor(rph*hrs)
        else:
            hascoin=True
        try:
            dummy=reward[mine['type']]
        except KeyError:
            if (math.floor(rph*hrs)>0):
                reward[mine['type']]=0
        reward[mine['type']]+=math.floor(rph*hrs)
    if hascoin:
        await gascoin.putmon(ctx,userid,reward['gascoin'])
    desc=''
    for item in reward.keys():
        desc+='`'+str(reward[item])+'x` **'+item+'**\n'
    await json.write('userinfo.json',userinfo)    
    await io.reply(ctx,'',await builder.buildDesc('Harvested Items',desc,1))
