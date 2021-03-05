import discord
from main.config import ownerID
from mute.mute import delMute
from iBot import client
from utils.functions import sendError, sendEmbed


@client.command()
async def unmute(ctx, member: discord.Member):

    perms = ctx.message.author.guild_permissions
    if ctx.message.author.id != ownerID and not perms.manage_messages:
        await sendError("You don't have permissions to use this command!", "", ctx)
        return

    await delMute(member.id, ctx.message.channel.guild.id)
    try:
        emoji = '\U0001F44D'
        await ctx.message.add_reaction(emoji)
        await sendEmbed(f"{member.mention} has successfully been soft muted!", "use `?iunmute @member` to unmute", ctx)
    except:
        await sendError("An error occurred!", "", ctx)


@unmute.error
async def unmute_error(ctx, error):
    await sendError("**Usage** ?iunmute @member\n**Example** ?iunmute @ibot\n\nSoft unmute a user.", "", ctx)