import discord
from discord.ext import commands

from main.config import ownerID
from mute.mute import delMute, isMuted
from iBot import client
from utils.functions import sendError, sendEmbed


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def unmute(ctx, member: discord.Member):

    perms = ctx.message.author.guild_permissions
    if ctx.message.author.id != ownerID and not perms.manage_messages:
        await sendError("You don't have permissions to use this command!", "", ctx)
        return

    if not await isMuted(member.id, ctx.message.channel.guild.id):
        await sendError("Member is not muted!", "", ctx)
        return

    await ctx.trigger_typing()
    await delMute(member.id, ctx.message.channel.guild.id)
    try:
        emoji = '\U0001F44D'
        await ctx.message.add_reaction(emoji)
        await sendEmbed(f"{member.mention} has successfully been soft unmuted!", "use imute @member to mute again!", ctx)
    except:
        await sendError("An error occurred!", "", ctx)


@unmute.error
async def unmute_error(ctx, error):
    await sendError("**Usage** iunmute `@member`\n**Example** iunmute `@ibot`\n\n`Soft unmute a user.`", "", ctx)