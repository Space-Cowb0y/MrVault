import discord
from discord.ext import commands

class TextCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.emojis = ()

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(334885839857516544)
        self.emojis = self.guild.emojis

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
