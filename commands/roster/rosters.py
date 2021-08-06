import discord
from discord.ext import commands

from iBot import client
from main.config import ownerID
from roster.roster import rosterlist
from utils.functions import sendError


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def rosters(ctx, ):
    perms = ctx.message.author.guild_permissions
    if ctx.message.author.id != ownerID and not perms.administrator:
        await sendError("You don't have permissions to use this command!", "", ctx)
        return

    lost_roster_list = await rosterlist(ctx.message.channel.guild.id)

    await ctx.trigger_typing()
    msg = ""
    for x in lost_roster_list:
        chan = client.get_channel(x.channel)
        role = ctx.message.channel.guild.get_role(x.role)
        msg += "`ID` **{0}** | `Roster` **{1}** | `Channel` **{2}** | `Role` **{3}**\n".format(x.id, x.header,
                                                                                               chan.mention,
                                                                                               role.mention)
    if len(lost_roster_list) == 0:
        msg = "No rosters available for this server\nUse `iroster` to create one!"

    em = discord.Embed(title='', description=msg, colour=0xe67e22)
    em.set_footer(text="To delete a roster use: idroster `ID`", icon_url=ctx.message.channel.guild.icon_url)
    await ctx.message.channel.send(embed=em)


@rosters.error
async def rosters_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        pass
    else:
        await sendError(f"Something went wrong...\nError log: {error}", "", ctx)
