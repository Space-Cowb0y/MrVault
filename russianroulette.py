import discord
from discord.ext import commands
import random

russian = [False,False,False,False,False,True]
random.shuffle(russian)

@commands.command()
async def rr(ctx):
    global russian
    if(russian.pop(0)): 
        russian = [False,False,False,False,False,True]
        random.shuffle(russian)
        await ctx.send("YOU DIED.")
    else:
        await ctx.send("THE GUN GOES CLICK. Remaining: " + str(len(russian)))