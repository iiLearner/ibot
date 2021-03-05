import discord
from iBot import client
from main.config import ownerID
from mute.mute import addMute
from utils.functions import sendError, sendEmbed


@client.command()
async def mute(ctx, member: discord.Member):
    perms = ctx.message.author.guild_permissions
    if ctx.message.author.id != ownerID and not perms.manage_messages:
        await sendError("You don't have permissions to use this command!", "", ctx)
        return

    myperms = ctx.message.channel.guild.me.guild_permissions
    if not myperms.manage_messages:
        await sendError("I need manage message permission in order to do this!", "", ctx)
        return

    await addMute(member.id, ctx.message.channel.guild.id, 0)

    try:
        emoji = '\U0001F44D'
        await ctx.message.add_reaction(emoji)
        await sendEmbed(f"{member.mention} has successfully been soft muted!", "use `?iunmute @member` to unmute", ctx)
    except:
        await sendError("An error occurred!")


@mute.error
async def mute_error(ctx, error):
    await sendError("**Usage** ?imute @member\n**Example** ?imute @ibot", "", ctx)


