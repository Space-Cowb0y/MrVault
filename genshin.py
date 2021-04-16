import discord
from discord.ext import commands, tasks
import pytz
import datetime
from enum import IntEnum

# TODO(#1): Cog it up.
# TODO(#2): Implement wishes.
# TODO(#3): Implement character and weapon stats.

server_times = {
                'NA': pytz.timezone('US/Central'),
                'EU': pytz.timezone('CET'),
                'ASIA': pytz.timezone('Asia/Shanghai'),
               }


class Days(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


fmt = '%-I:%M %p'


def formatTimedelta(timedelta):
    s = timedelta.seconds
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)

    hoursfmt = "hora" if hours <= 1 else "horas"
    minutesfmt = "minuto" if minutes <= 1 else "minutos"

    if(hours > 0 and minutes > 0):
        return '{0} {1} e {2} {3}'.format(hours, hoursfmt, minutes, minutesfmt)
    elif(hours > 0 and minutes == 0):
        return '{0} {1}'.format(hours, hoursfmt)
    else:
        return '{0} {1}'.format(minutes, minutesfmt)


def labelFormatText(label, time):
    return "```fix\n# {0} {1}```".format(label, time)


def timeFormatText(formatted_time_delta, is_weekly=False, days=0):
    if(is_weekly):
        if(days == 0):
            return(
                "\u2022 {0} at\u00e9 o reset semanal"
                .format(formatted_time_delta)
            )
        else:
            if("hora" not in formatted_time_delta):
                return(
                    "\u2022 {0} dias e {1} at\u00e9 o reset semanal"
                    .format(days, formatted_time_delta)
                )
            else:
                return(
                    "\u2022 {0} dias, {1} at\u00e9 o reset semanal".
                    format(days, formatted_time_delta)
                )
    else:
        return(
            "\u2022 {0} at\u00e9 o reset diário"
            .format(formatted_time_delta)
        )


def calcDeltaDays(reset_weekday, time_now, timedelta_days, reset_hour=4):
    delta_days = ((reset_weekday - time_now.weekday()) % 7) + timedelta_days
    if(delta_days <= 0 and time_now.hour > reset_hour):
        delta_days = 6
    elif(delta_days <= 0):
        delta_days = 0
    return delta_days


def createEmbed():

    embed = discord.Embed(title='Timers')
    embed.description = ""

    for server in server_times:
        time_now = datetime.datetime.now(tz=server_times[server])
        reset_datetime = time_now.replace(hour=4,
                                          minute=0,
                                          second=0,
                                          microsecond=0)
        deltatime_until_reset = reset_datetime - time_now
        delta_days = calcDeltaDays(Days.MONDAY,
                                   time_now,
                                   deltatime_until_reset.days)

        embed.description += labelFormatText(server, time_now.strftime(fmt))
        embed.description += timeFormatText(
            formatTimedelta(deltatime_until_reset)
        ) + "\n"
        embed.description += timeFormatText(
            formatTimedelta(deltatime_until_reset),
            is_weekly=True,
            days=delta_days
        )

    embed.description += labelFormatText("HoYoLab Daily Check-In",
                                         time_now.strftime(fmt))
    checkin_reset_time = time_now.replace(hour=0,
                                          minute=0,
                                          second=0,
                                          microsecond=0)
    checkin_time_left = checkin_reset_time - time_now
    embed.description += timeFormatText(formatTimedelta(checkin_time_left))

    time_now = datetime.datetime.now(tz=server_times["NA"])
    embed.description += labelFormatText("NPCs Vendedores de Artefatos",
                                         time_now.strftime(fmt))

    artifact_reset_time = time_now.replace(hour=4,
                                           minute=0,
                                           second=0,
                                           microsecond=0)
    delta_time = artifact_reset_time - time_now
    delta_days = calcDeltaDays(Days.THURSDAY,
                               time_now,
                               delta_time.days)
    embed.description += timeFormatText(formatTimedelta(delta_time),
                                        is_weekly=True,
                                        days=delta_days)

    embed.set_image(url='https://i.imgur.com/CYvBWxw.png')
    embed.timestamp = datetime.datetime.now(
        tz=pytz.timezone('America/Sao_Paulo')
    )
    embed.set_footer(text='%gt,%genshin,%time')
    return embed


@commands.command(aliases=['gt', 'genshin', 'time'])
async def genshin_time(ctx):
    await ctx.send(embed=createEmbed())


class EditCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 781588371377356812
        self.message_id = 822931171566026792
        self.edit.start()

    @tasks.loop(minutes=2, seconds=30)
    async def edit(self):
        channel = self.bot.get_channel(self.channel_id)
        message = await channel.fetch_message(self.message_id)
        await message.edit(embed=createEmbed())

    @edit.before_loop
    async def before_edit(self):
        await self.bot.wait_until_ready()
