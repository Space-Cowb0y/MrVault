import discord
from discord.ext import commands
import russianroulette
import genshin
import fun

bot = commands.Bot(command_prefix='%')

bot.add_command(russianroulette.rr)
bot.add_command(genshin.genshin_time)
bot.add_cog(genshin.EditCog(bot))
bot.add_cog(fun.TextCog(bot))
bot.run('NzM3ODQyNzA4MjgxOTUwMjk5.XyDPkg.lSPG7hYvg9XV15UuCLXdCSk2sXU')
