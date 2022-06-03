import jsonprocessor as json
import discordio as io
import embedbuilder as builder

import math
import time

async def mute(ctx,userid,duration):
    muted=await json.read('muted.json')
    try:
        dummy=muted[userid]
    except:
        muted[userid]=0
    muted[userid]=math.ceil(time.time())
    muted[userid]+=duration
    await io.reply(ctx,'',await builder.buildDesc('Mute Successful','<@'+userid+'>\'s mute is now muted until <t:'+str(muted[userid])+':f>',1))
    await json.write('muted.json',muted)