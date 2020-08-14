import discord
from discord.ext import commands
import urllib, json
import random
lines = []
with open('c:/users/thiag/Desktop/yugioh archetypes.txt') as fp:
    line = fp.readline()
    while line:
        lines.append(line.replace('\n',''))
        line = fp.readline()

@commands.command()
async def rand(ctx):
    embed = discord.Embed(type='rich')
    archtype = random.choice(lines)
    embed.title = archtype
    embed.url = "https://yugioh.fandom.com/wiki/List_of_%22" +  archtype.replace(' ','_') + '%22_cards'
    await ctx.send(embed=embed)

@commands.command()
async def card(ctx, *args):
    hdrs = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}
    request = urllib.request.Request(url="https://db.ygoprodeck.com/api/v7/cardinfo.php?name=" + '%20'.join(args), headers=hdrs)
    try:
        with urllib.request.urlopen(request) as url:
            resp = json.loads(url.read().decode())
    except urllib.error.HTTPError:
        print("Fallback to fuzzy search!")
        request = urllib.request.Request(url="https://db.ygoprodeck.com/api/v7/cardinfo.php?fname=" + '%20'.join(args), headers=hdrs) 
        try:
            with urllib.request.urlopen(request) as url:
                resp = json.loads(url.read().decode())
        except urllib.error.HTTPError as e:
            embed = discord.Embed(title='Cat.exe has stopped working')
            embed.set_thumbnail(url='https://i.imgur.com/MoEWqyg.gif')
            embed.description = 'As crianças chinesas escravas não conseguiram encontrar o que você queria. Providências já foram tomadas, tente novamente com outro termo!'
            embed.add_field(name='Exceção',value=e.__str__())
            #print(str(e.with_traceback()))
            await ctx.send(embed=embed)
            return
            
    data = resp.get('data')
    firstCard = data[0]
    embed = discord.Embed(title=firstCard.get('name'))
    embed.add_field(name='Type',value=firstCard.get('race') + ' ' + firstCard.get('type'))
    if('archetype' in firstCard):
        embed.add_field(name='Archetype',value=firstCard.get('archetype'))
    if ('Monster' in firstCard.get('type')):
        if('XYZ' in firstCard.get('type')):
            embed.add_field(name='Rank',value=firstCard.get('level'))
        else:
            embed.add_field(name='Level',value=firstCard.get('level'))
        embed.add_field(name='Attribute',value=firstCard.get('attribute'))
        if('Link' in firstCard.get('type')):
            atkdef = str(firstCard.get('atk'))
            embed.add_field(name='ATK',value=atkdef)
        else:
            atkdef = str(firstCard.get('atk')) + '/' + str(firstCard.get('def'))
            embed.add_field(name='ATK/DEF',value=atkdef)
        if('Pendulum' in firstCard.get('type')):
            embed.add_field(name='Scales',value=firstCard.get('scale'))
        elif('Link' in firstCard.get('type')):
            embed.remove_field(1) #remove Level field
            embed.add_field(name='Link Value',value=firstCard.get('linkval'))
            embed.add_field(name='Link Markers',value=', '.join(firstCard.get('linkmarkers')))
    embed.add_field(name='Card Text', value=firstCard.get('desc'),inline=False)
    embed.set_thumbnail(url=firstCard.get('card_images')[0].get('image_url'))
    await ctx.send(embed=embed)
