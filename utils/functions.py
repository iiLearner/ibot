import discord
import mysql.connector
import os
from iBot import client


def is_bot(m):
    return m.author == client.user


async def sendEmbed(message: str, footer: str, ctx):
    em = discord.Embed(title='', description=message, colour=0x2ecc71)
    em.set_footer(text=footer, icon_url=client.user.avatar_url)
    await ctx.message.channel.send(embed=em)


async def sendError(message: str, footer: str, ctx):
    em = discord.Embed(title='', description=message, colour=0xe74c3c)
    em.set_footer(text=footer, icon_url=client.user.avatar_url)
    await ctx.message.channel.send(embed=em)


async def dbConnect():
    mydb = mysql.connector.connect(
        host=os.getenv("MySQLhost"),
        user=os.getenv("MySQLuser"),
        passwd=os.getenv("MySQLpasswd"),
        db=os.getenv("MySQLdb")
    )
    return mydb
