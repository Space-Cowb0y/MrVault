from discord.ext import commands
import upsidedown

@commands.command()
async def flip(ctx, *args):
    await ctx.send('(╯°□°）╯︵ ' + upsidedown.transform(' '.join(args)))