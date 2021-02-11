import discord
from discord.ext import commands
from emojis.emoji import delete_emoji
from main.config import ownerID
from iBot import client


@client.command()
async def removeuser(ctx, member: discord.Member, emoji: discord.Emoji):
    if ctx.message.author.id != ownerID:
        await ctx.message.channel.send("no")
        return
    try:
        await delete_emoji(emoji.id, member.id, ctx.message.channel.guild.id)
        await ctx.message.channel.send("Successfully removed {} from the list".format(member.mention))
    except:
        await ctx.message.channel.send("Operation failed")


@removeuser.error
async def removeuser_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.message.channel.send("**Usage** ?removeuser @user")
    else:
        await ctx.message.channel.send("**Usage** ?removeuser @user")
