import embedbuilder as builder
import discordio as io
import jsonprocessor as json
import gascoinprocess as gascoin
import asyncio
import random as rd

async def printBoard(ctx,userid):
    emotes=await json.read('emotes.json')
    playerdata=await json.read('minesweeper.json')
    board=playerdata[userid]['board']
    status=playerdata[userid]['status']
    output=''
    for i in range(1,len(board)-1):
        for j in range(1,len(board[i])-1):
            if (status[i][j]=='S'):
                output+=emotes[str(board[i][j])]
            else:
                output+=emotes[status[i][j]]
        output+='\n'
    msgid=await io.reply(ctx,'',await builder.buildDesc(str(ctx.author.name)+'\'s Minesweeper Board',output,1))
    await asyncio.sleep(30)
    msg=await ctx.fetch_message(msgid)
    await msg.delete()

async def openCell(ctx,userid,x,y,init=True):
    playerdata=await json.read('minesweeper.json')
    if not (playerdata[userid]['hasboard']):
        await io.reply(ctx,'',await builder.buildDesc('Game Not Found','You haven\'t started a game yet!',0))
        return False
    board=playerdata[userid]['board']
    status=playerdata[userid]['status']
    if (min(x,y)<1) or (max(x,y)>len(board)-2):
        if (init):
            await io.reply(ctx,'',await builder.buildDesc('Invalid Selection','Cell out of bound',0))
        return True
    if (status[x][y]!='H'):
        if (init):
            await io.reply(ctx,'',await builder.buildDesc('Invalid Selection','Cell already opened/flagged',0))
        return True
    status[x][y]='S'
    if (board[x][y]==-1):
        playerdata[userid]['hasboard']=False
        for i in range(1,len(board)-1):
            for j in range(1,len(board)-1):
                status[i][j]='S'
        await json.write('minesweeper.json',playerdata)
        await printBoard(ctx,userid)
        await io.reply(ctx,'',await builder.buildDesc('You Lost','',0))
        await gascoin.putmon(ctx,userid,(2*playerdata[userid]['corrflagcnt']-playerdata[userid]['flagcap'])*10)
        return False
    await json.write('minesweeper.json',playerdata)
    if (board[x][y]!=0):
        return True
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if (i!=x) or (j!=y):
                await openCell(ctx,userid,i,j,False)
    return True

async def flagCell(ctx,userid,x,y):
    playerdata=await json.read('minesweeper.json')
    if not (playerdata[userid]['hasboard']):
        await io.reply(ctx,'',await builder.buildDesc('Game Not Found','You haven\'t started a game yet!',0))
        return False
    if (playerdata[userid]['flagcnt']==playerdata[userid]['flagcap']):
        await io.reply(ctx,'',await builder.buildDesc('Flag Limit Reached','Please unflag some cells first!',0))
        return True
    board=playerdata[userid]['board']
    status=playerdata[userid]['status']
    if (min(x,y)<1) or (max(x,y)>len(board)-2):
        await io.reply(ctx,'',await builder.buildDesc('Invalid Selection','Cell out of bound',0))
        return True
    if (status[x][y]!='H'):
        await io.reply(ctx,'',await builder.buildDesc('Invalid Selection','Cell already opened/flagged',0))
        return True
    status[x][y]='F'
    playerdata[userid]['flagcnt']+=1
    if (board[x][y]==-1):
        playerdata[userid]['corrflagcnt']+=1
    if (playerdata[userid]['corrflagcnt']==playerdata[userid]['flagcap']):
        await json.write('minesweeper.json',playerdata)
        await printBoard(ctx,userid)
        await io.reply(ctx,'',await builder.buildDesc('You Win','',1))
        await gascoin.putmon(ctx,userid,playerdata[userid]['flagcap']*20)
        return False
    await json.write('minesweeper.json',playerdata)
    return True

async def unflagCell(ctx,userid,x,y):
    playerdata=await json.read('minesweeper.json')
    if not (playerdata[userid]['hasboard']):
        await io.reply(ctx,'',await builder.buildDesc('Game Not Found','You haven\'t started a game yet!',0))
        return False
    board=playerdata[userid]['board']
    status=playerdata[userid]['status']
    if (min(x,y)<1) or (max(x,y)>len(board)-2):
        await io.reply(ctx,'',await builder.buildDesc('Invalid Selection','Cell out of bound',0))
        return True
    if (status[x][y]!='F'):
        await io.reply(ctx,'',await builder.buildDesc('Invalid Selection','Cell is not flagged',0))
        return True
    status[x][y]='H'
    playerdata[userid]['flagcnt']-=1
    if (board[x][y]==-1):
        playerdata[userid]['corrflagcnt']-=1
    await json.write('minesweeper.json',playerdata)
    return True

async def makeBoard(userid,size,mcnt):
    board=[]
    status=[]
    for i in range(size+2):
        board.append([])
        status.append([])
        for j in range(size+2):
            board[i].append(0)
            status[i].append('H')
    mines=[]
    for i in range(mcnt):
        exist=True
        while (exist):
            x=rd.randint(1,size)
            y=rd.randint(1,size)
            exist=False
            for j in range(0,i):
                if (x==mines[j][0]) and (y==mines[j][1]):
                    exist=True
            if ((x==y) and ((x==1) or (x==size))) or ((x+y==size+1) and ((x==1) or (x==size))):
                exist=True
        mines.append([x,y])
        board[x][y]=-1
        for j in range(x-1,x+2):
            for k in range(y-1,y+2):
                if (board[j][k]!=-1):
                    board[j][k]+=1
    playerdata=await json.read('minesweeper.json')
    playerdata[userid]={}
    playerdata[userid]['hasboard']=True
    playerdata[userid]['flagcnt']=0
    playerdata[userid]['flagcap']=mcnt
    playerdata[userid]['corrflagcnt']=0
    playerdata[userid]['board']=board
    playerdata[userid]['status']=status
    await json.write('minesweeper.json',playerdata)

async def listdiff(ctx):
    desc=''
    desc+='**Easy**: `5x5 board`, `4 mines`.\n'
    desc+='**Medium**: `8x8 board`, `12 mines`.\n'
    desc+='**Hard**: `10x10 board`, `23 mines`.\n'
    desc+='**Extreme**: `14x14 board`, `36 mines`.\n'
    await io.reply(ctx,'',await builder.buildDesc('Minesweeper Difficulty',desc,1))