import discord
from discord.ext import commands
#import yugioh
#import Flip
import russianroulette
import genshin
bot = commands.Bot(command_prefix='%')

#bot.add_command(yugioh.rand)
#bot.add_command(Flip.flip)
#bot.add_command(yugioh.card)
bot.add_command(russianroulette.rr)
bot.add_command(genshin.genshin_time)
bot.add_cog(genshin.EditCog(bot))

bot.run('NzM3ODQyNzA4MjgxOTUwMjk5.XyDPkg.9bS0EMpn9Y9gerpPJnSddRfrWCQ')
