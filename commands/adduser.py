import discord
from discord.ext import commands

from emojis.emoji import save_emoji, Emoji
from main.config import ownerID
from iBot import client


@client.command()
async def adduser(ctx, member: discord.Member, emoji: discord.Emoji):
    if ctx.message.author.id != ownerID:
        await ctx.message.channel.send("no")
        return
    try:
        await save_emoji(Emoji(emoji.id, member.id, ctx.message.channel.guild.id))
        await ctx.message.channel.send("Successfully added {} to the list with {}".format(member.mention, emoji))
    except:
        await ctx.message.channel.send("Operation failed")


@adduser.error
async def adduser_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.message.channel.send("**Usage** ?adduser @user emoji")
    else:
        await ctx.message.channel.send("**Usage** ?adduser @user emoji")
