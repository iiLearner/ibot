import discord

from iBot import client
from roster.roster import add_roster, rosterlist, del_roster
from utils.functions import sendEmbed, sendError


@client.command()
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
                    msg = "No rosters available for this server\nUse `?roster` to create one!"

                em = discord.Embed(title='', description=msg, colour=0xe67e22)
                em.set_footer(text="To delete a roster use: ?droster ID", icon_url=ctx.message.channel.guild.icon_url)
                await ctx.message.channel.send(embed=em)
            else:
                await sendError("Something went wrong..", "", ctx)
            return

    await sendError("I could not find that roster in this server", "", ctx)


@client.command()
async def rosters(ctx, ):
    perms = ctx.message.author.guild_permissions
    if not perms.administrator:
        await ctx.message.channel.send("**[ERROR]** You must be a server admin in order to do this")
        return

    lost_roster_list = await rosterlist(ctx.message.channel.guild.id)

    msg = ""
    for x in lost_roster_list:
        chan = client.get_channel(x.channel)
        role = ctx.message.channel.guild.get_role(x.role)
        msg += "`ID` **{0}** | `Roster` **{1}** | `Channel` **{2}** | `Role` **{3}**\n".format(x.id, x.header,
                                                                                               chan.mention,
                                                                                               role.mention)
    if len(lost_roster_list) == 0:
        msg = "No rosters available for this server\nUse `?roster` to create one!"

    em = discord.Embed(title='', description=msg, colour=0xe67e22)
    em.set_footer(text="To delete a roster use: ?droster ID", icon_url=ctx.message.channel.guild.icon_url)
    await ctx.message.channel.send(embed=em)


@client.command()
async def roster(ctx, channel: discord.TextChannel, role: discord.Role):
    perms = ctx.message.author.guild_permissions
    tick_emoji = client.get_emoji(806114376297611266)
    redtick_emoji = client.get_emoji(806117763784638464)

    if not perms.administrator:
        await ctx.message.channel.send("**[ERROR]** You must be a server admin in order to create a roster")
        return
    await sendEmbed("Welcome to iBot's Clan Roster Setup\nPlease type the header of the roster (top text)\n\
                    **Example** My Clan Members", "", ctx)

    def check(m):
        return m.author == ctx.message.author and m.channel == ctx.message.channel

    msg = await client.wait_for('message', check=check)
    if len(msg.content) > 100:
        await sendError("The header must be less than 200 characters!", "", ctx)
        return
    await msg.add_reaction(tick_emoji)

    clan_emoji = client.get_emoji(702314132933836970)
    await sendEmbed("Please type the clan symbol/emoji: \n**Example** 頑 or {0}".format(clan_emoji), "", ctx)
    symbol = await client.wait_for('message', timeout=60.0, check=check)
    if len(symbol.content) > 200:
        await sendError("The symbol must be less than 200 characters!", "", ctx)
        return
    await symbol.add_reaction(tick_emoji)

    await sendEmbed("Please type the roster colour RGB:\n**Example** 0x9b59b6", "", ctx)
    color = await client.wait_for('message', timeout=60.0, check=check)
    await color.add_reaction(tick_emoji)
    readableHex = int(hex(int(color.content.replace("#", ""), 16)), 0)

    await ctx.message.channel.send("Example of how it will look like:")
    example_msg = '**{0}**\n\n{1} **{2}**'.format(msg.content, symbol.content, "iLearner")
    em = discord.Embed(title='', description=example_msg, colour=readableHex)
    await ctx.message.channel.send(embed=em)
    msg_confirm = await ctx.message.channel.send("React with {0} to confirm!".format(tick_emoji))
    await msg_confirm.add_reaction(tick_emoji)
    await msg_confirm.add_reaction(redtick_emoji)

    def check(reac, reacuser):
        return reacuser == ctx.message.author

    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    if reaction.emoji == tick_emoji:
        example_msg = "**{0}**\n\n".format(msg.content)
        for member in ctx.message.channel.guild.members:
            for mrole in member.roles:
                if mrole.id == role.id:
                    example_msg += '{0} **{1}**\n'.format(symbol.content, member.name)
        example_msg += "\n\n"
        em = discord.Embed(title='', description=example_msg, colour=readableHex)
        msg_id = await channel.send(embed=em)
        added = await add_roster(ctx.message.channel.guild.id, channel.id, role.id, msg_id.id, msg.content, symbol.content,
                                 color.content)
        if added:
            await sendEmbed("Setup complete!\nUse `?rosters` to see the list of rosters", "", ctx)
        else:
            await sendError("Something went wrong...", "", ctx)
            await msg_id.delete()
    else:
        await ctx.message.channel.send("Setup aborted!")


# errors"""
@roster.error
async def roster_error(ctx, error):
    await sendError("**Usage** ?roster #channel @role\n**Example** ?roster #roster @clanmembers", "", ctx)


@rosters.error
async def rosters_error(ctx, error):
    await sendError("Something went wrong...", "", ctx)


@droster.error
async def droster_error(ctx, error):
    await sendError("**Usage** ?droster ID\n**Example** ?droster 1", "", ctx)