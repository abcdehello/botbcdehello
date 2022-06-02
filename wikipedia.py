import requests
import discordio as io
import embedbuilder as builder

async def search(ctx,title):
    response=requests.get('https://en.wikipedia.org/w/api.php?origin=*&action=query&list=search&format=json&srsearch='+title).json()
    desc='There are '+str(response['query']['searchinfo']['totalhits'])+' results on the title `'+title+'`.\n'
    exactMatch=False
    for article in response['query']['search']:
        if (article['title'].lower()==title.lower()):
            desc+='Found exact match of title '+title+':\n'
            desc+='https://en.wikipedia.org/wiki/'
            for i in title:
                if (i==' '):
                    desc+='_'
                else:
                    desc+=i
            exactMatch=True
    if not (exactMatch):
        desc+='There are no exact matches of title '+title+'\n'
    await io.reply(ctx,'',await builder.buildDesc('Search Result of '+title+' on Wikipedia',desc,1))
