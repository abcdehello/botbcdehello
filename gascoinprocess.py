import discordio as io
import embedbuilder as builder
from pymongo import MongoClient
cluster=MongoClient("mongodb+srv://gasbug:20062006@gas-coins.dpdvj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=cluster["discord_bot"]
collection=db["coins"]
async def getmon(userid):
    result=collection.find_one({"_id":str(userid)})
    try:
        return result["money"]
    except:
        temp={"_id":str(userid),"money":0.0}
        collection.insert_one(temp)
        return 0
async def putmon(ctx,userid,amount):
    await getmon(userid)
    collection.update_one({"_id":str(userid)},{"$inc":{"money":amount}})
    if (amount>=0):
        await io.reply(ctx,'',await builder.buildDesc('You Earned Gascoins','You gained '+str(int(amount))+' <:gascoin:981542532586569808>',1))
    else:
        await io.reply(ctx,'',await builder.buildDesc('You Lost Gascoins','You lost '+str(-int(amount))+' <:gascoin:981542532586569808>',1))
