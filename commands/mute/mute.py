import discord
from discord.ext import commands

from iBot import client
from main.config import ownerID
from mute.mute import addMute, isMuted
from utils.functions import sendError, sendEmbed


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def mute(ctx, member: discord.Member):
    perms = ctx.message.author.guild_permissions
    if ctx.message.author.id != ownerID and not perms.manage_messages:
        await sendError("You don't have permissions to use this command!", "", ctx)
        return

    myperms = ctx.message.channel.guild.me.guild_permissions
    if not myperms.manage_messages:
        await sendError("I need manage message permission in order to do this!", "", ctx)
        return

    if await isMuted(member.id, ctx.message.channel.guild.id):
        await sendError("Member is already muted!", "", ctx)
        return

    if member.bot:
        await sendError("You cannot mute a bot!", "", ctx)
        return

    await ctx.trigger_typing()
    await addMute(member.id, ctx.message.channel.guild.id, 0)
    try:
        emoji = '\U0001F44D'
        await ctx.message.add_reaction(emoji)
        await sendEmbed(f"{member.mention} has successfully been soft muted!", "use iunmute @member to unmute", ctx)
    except:
        await sendError("An error occurred!")


@mute.error
async def mute_error(ctx, error):
    await sendError("**Usage** imute `@member`\n**Example** imute `@ibot`\n\n`Soft mute a user. Soft muting a user will result in user messages being immediately deleted!`", "", ctx)


