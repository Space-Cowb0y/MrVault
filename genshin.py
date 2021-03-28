import discord
from discord.ext import commands, tasks
import pytz
import datetime

# TODO(#1): Cog it up.
# TODO(#2): Implement wishes.
# TODO(#3): Implement character and weapon stats.
# TODO(#4): Add weekly reset timer.

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
    if(hours > 0 and minutes > 0):
        return '{} horas e {} minutos at\u00e9 o reset'.format(hours,minutes)
    elif(hours > 0 and minutes == 0):
        return '{} horas at\u00e9 o reset'
    else:
        return '{} minutos at\u00e9 o reset'.format(minutes)

def createEmbed():

    today = datetime.datetime.today().weekday()
    time_now = datetime.datetime.now()
    embed = discord.Embed(title='Timers')
    embed.description = ""

    for server in server_times:
        time_now = datetime.datetime.now(tz=server_times[server])
        reset_datetime = time_now.replace(hour=4,minute=0,second=0,microsecond=0)
        deltatime_until_reset = reset_datetime - time_now
        server_time_line = "```fix\n# {0} {1}```".format(server,
                                                    time_now.strftime(fmt),
                                                   )
        time_left_line = "\u2022 {0} di\u00e1rio".format(formatTimedelta(deltatime_until_reset))
        embed.description = embed.description + server_time_line + time_left_line


    daily_checkin_line = "```fix\n# {0} {1}```".format("HoYoLab Daily Check-In", time_now.strftime(fmt))
    checkin_reset_time = time_now.replace(hour=0,minute=0,second=0,microsecond=0)
    checkin_time_left = checkin_reset_time - time_now
    checkin_timeleft_line = "\u2022 {0} di\u00e1rio".format(formatTimedelta(checkin_time_left))

    time_now = datetime.datetime.now(tz=server_times["NA"])
    artifact_line = "```fix\n# {0} {1}```".format("NPCs Vendedores de Artefatos", time_now.strftime(fmt))

    artifact_reset_time = time_now.replace(hour=4,minute=0, second=0, microsecond=0)
    delta_time = artifact_reset_time - time_now
    delta_days = abs(today - 3)
    artifact_reset_line = "\u2022 {0} dias, {1} semanal".format(delta_days, formatTimedelta(delta_time))

    embed.description = embed.description + daily_checkin_line + checkin_timeleft_line + artifact_line + artifact_reset_line

    embed.set_image(url='https://i.imgur.com/40UEepe.png')
    embed.timestamp = datetime.datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
    embed.set_footer(text='%gt,%genshin,%time')
    return embed

@commands.command(aliases=['gt','genshin','time'])
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
