import discord
from discord.ext import commands

from iBot import client
from roster.roster import rosterlist, del_roster
from utils.functions import sendEmbed, sendError


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def droster(ctx, roster_id: int):
    perms = ctx.message.author.guild_permissions
    if not perms.administrator:
        await ctx.message.channel.send("**[ERROR]** You must be a server admin in order to do this")
        return

    lost_roster_list = await rosterlist(ctx.message.channel.guild.id)
    for r in lost_roster_list:
        if r.id == roster_id:
            deleted = await del_roster(roster_id)
            if deleted:
                await sendEmbed("Roster deleted successfully!", "", ctx)
                lost_roster_list.remove(r)
                msg = ""
                for x in lost_roster_list:
                    chan = client.get_channel(x.channel)
                    role = ctx.message.channel.guild.get_role(x.role)
                    msg += "`ID` **{0}** | `Roster` **{1}** | `Channel` **{2}** | `Role` **{3}**\n".format(x.id,
                                                                                                           x.header,
                                                                                                           chan.mention,
                                                                                                           role.mention)
                if len(lost_roster_list) == 0:
                    msg = "No rosters available for this server\nUse `iroster` to create one!"

                em = discord.Embed(title='', description=msg, colour=0xe67e22)
                em.set_footer(text="To delete a roster use: idroster ID", icon_url=ctx.message.channel.guild.icon_url)
                await ctx.message.channel.send(embed=em)
            else:
                await sendError("Something went wrong..", "", ctx)
            return

    await sendError("I could not find that roster in this server", "", ctx)


@droster.error
async def droster_error(ctx, error):
    await sendError("**Usage** idroster `ID`\n**Example** idroster `1`\n\n`Delete a roster from your server`", "Provide the roster ID (`irosters` to see IDs)", ctx)
