import discord

from iBot import client
from main.config import ownerID
from mute.mute import addMute, delMute
from utils.functions import sendError


@client.command()
async def imute(ctx, member: discord.Member, flag=None):
    if ctx.message.author.id != ownerID:
        await ctx.message.channel.send("no")
        return

    if flag is None:
        await addMute(member.id, ctx.message.channel.guild.id, 0)
    else:
        await addMute(member.id, ctx.message.channel.guild.id, 1)

    emoji = '\U0001F44D'
    await ctx.message.add_reaction(emoji)


@client.command()
async def iunmute(ctx, member: discord.Member):
    if ctx.message.author.id != ownerID:
        await ctx.message.channel.send("no")
        return

    await delMute(member.id)
    try:
        emoji = '\U0001F44D'
        await ctx.message.add_reaction(emoji)
    except:
        pass


@imute.error
async def iunmute_error(ctx, error):
    await sendError("**Usage** ?imute @member\n**Example** ?imute @ibot", "", ctx)


@iunmute.error
async def imute_error(ctx, error):
    await sendError("**Usage** ?iunmute @member\n**Example** ?iunmute @ibot", "", ctx)

