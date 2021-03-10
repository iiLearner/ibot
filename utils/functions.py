import discord
import mysql.connector
import os
from iBot import client
import asyncio


def is_bot(m):
    return m.author == client.user


async def sendEmbed(message: str, footer: str, ctx):
    em = discord.Embed(title='', description=message, colour=0x2ecc71)
    em.set_footer(text=footer, icon_url=client.user.avatar_url)
    await ctx.message.channel.send(embed=em)


async def sendError(message: str, footer: str, ctx):
    em = discord.Embed(title='', description=message, colour=0xe74c3c)
    em.set_footer(text=footer, icon_url=client.user.avatar_url)
    message = await ctx.message.channel.send(embed=em)
    return message


async def sendCooldown(time: str, ctx):
    emoji = '\U0001f55b'
    em = discord.Embed(title='', description=f"{emoji} Please wait {round(time, 2)}s and try again!", colour=0xe67e22)
    em.set_author(name="Cooldown!", icon_url=ctx.message.author.avatar_url)
    message = await ctx.message.channel.send(embed=em)
    await asyncio.sleep(int(time))
    await message.delete()


async def getWelcomeChannel(guild):
    for channel in guild.channels:
        if channel.name is "general":
            return channel

    if guild.system_channel is not None:
        return guild.system_channel

    return guild.channels[0]


async def sendHelpMessage(channel):

    message = "Here is the list of commands!\nFor more info on a command, use `{command}` to view usage help.\nFor further assistance join our [guild](https://discord.gg/79kbdEDwnV)\n\n"
    em = discord.Embed(title='', description=message, colour=0xe67e22)
    em.set_author(name="Command help", icon_url=channel.guild.icon_url)

    emoji = client.get_emoji(788351325531537428)
    em.add_field(name=f"{emoji} Emoji", value="`addemoji` `delemoji`", inline=False)

    emoji = client.get_emoji(777915907644850227)
    em.add_field(name=f"{emoji} Roster", value="`roster` `droster` `rosters`", inline=False)

    emoji = client.get_emoji(817499208189345882)
    em.add_field(name=f"{emoji} Tournament", value="`create_tourney` `cancel_tourney` `tourney_role` `close_tourney` `sendkeys`", inline=False)

    emoji = client.get_emoji(565838171363868682)
    em.add_field(name=f"{emoji} Special Mute", value="`mute` `unmute`", inline=False)

    emoji = client.get_emoji(817523844004053044)
    em.add_field(name=f"{emoji} Minecraft", value="`server`", inline=False)

    em.set_footer(text="You must use `i` prefix before the commands!", icon_url=client.user.avatar_url)
    await channel.send(embed=em)


# escape strings before inserting into databases. avoids errors and possible security faults.
def escape_string(string: str):
    escaped = string.translate(str.maketrans(
        {"-": r"\-", "]": r"\]", "\\": r"\\", "^": r"\^", "$": r"\$", "'": r"\'", "*": r"\*", ".": r"\."}))
    return escaped

async def dbConnect():
    mydb = mysql.connector.connect(
        host=os.getenv("MySQLhost"),
        user=os.getenv("MySQLuser"),
        passwd=os.getenv("MySQLpasswd"),
        db=os.getenv("MySQLdb")
    )
    return mydb
