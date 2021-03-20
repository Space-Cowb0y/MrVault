import discord
from discord.ext import commands, tasks
import pytz
import datetime

server_times = {
                'NA':pytz.timezone('US/Central'),
                'EU':pytz.timezone('CET'),
                'ASIA':pytz.timezone('Asia/Shanghai'),
              }
fmt = '%-I:%M %p'
def formatTimedelta(timedelta):
    s = timedelta.seconds
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    if(hours > 0):
        return '{} horas e {} minutos at\u00e9 o reset di\u00e1rio'.format(hours,minutes)
    else:
        return '{} minutos at\u00e9 o reset di\u00e1rio'.format(minutes)

def createEmbed():
    embed = discord.Embed(title='Server Time')
    embed.description = ""
    for server in server_times:
        time_now = datetime.datetime.now(tz=server_times[server])
        reset_datetime = time_now.replace(hour=4,minute=0,second=0,microsecond=0)
        deltatime_until_reset = reset_datetime - time_now
        server_time_line = "```fix\n# {0} {1}```".format(server,
                                                    time_now.strftime(fmt),
                                                   )
        time_left_line = "\u2022 {0}".format(formatTimedelta(deltatime_until_reset))
        embed.description = embed.description + server_time_line +  time_left_line
        embed.set_image(url='https://i.ytimg.com/vi/TSsWsCdiiPI/maxresdefault.jpg')
        embed.timestamp = datetime.datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
    return embed
@commands.command()
async def genshin_time(ctx):
    await ctx.send(embed=createEmbed())
class EditCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.channel_id = 781588371377356812
        self.message_id = 822931171566026792
        self.edit.start()
    @tasks.loop(minutes=2,seconds=30)
    async def edit(self):
        channel = self.bot.get_channel(self.channel_id)
        message = await channel.fetch_message(self.message_id)
        await message.edit(embed=createEmbed())
    @edit.before_loop
    async def before_edit(self):
        await self.bot.wait_until_ready()
