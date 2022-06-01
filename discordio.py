import discord

async def reply(ctx,message,embed):
  msg = await ctx.reply(message,embed=embed,mention_author=False)
  return msg.id

async def edit(ctx,id,message,embed):
  editmsg=await ctx.fetch_message(id)
  await editmsg.edit(content=message,embed=embed,mention_author=False)