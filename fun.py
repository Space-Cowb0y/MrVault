import discord
from discord.ext import commands
import random

class TextCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = ()

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(334885839857516544)
        self.emojis = guild.emojis

    @commands.command()
    async def omega(self, ctx, *args):
        omegalul = None
        for e in self.emojis:
            if(e.name == 'OMEGALUL'):
                omegalul = e
        if(omegalul):
            omegafied = ' '.join(args).replace('o',str(omegalul)).replace('O', str(omegalul))
            await ctx.send(omegafied)
        else:
            await ctx.send(' '.join(args))

    @commands.command()
    async def decida(self,ctx,*args):
        if(len(args) < 2):
            await ctx.send('Cara, tu n\u00e3o me deu escolhas o suficiente')
        else:
            random.seed()

            listArgs = list(args)
            listArgs.append("")

            listArgsLen = len(listArgs)
            no_pick_weight = 1/listArgsLen/2
            weight = 1 - no_pick_weight
            prob = []

            for i in range(0,listArgsLen - 1):
                prob.append(weight)

            prob.append(no_pick_weight)

            choice = random.choices(listArgs, weights=prob, k = 1)
            if(choice[0] == ""):
                await ctx.send('Prefiro n\u00e3o escolher!')
            else:
                await ctx.send('Decidi ' + choice[0])
