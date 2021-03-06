import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import ColourConverter

from iBot import client
from roster.roster import add_roster
from utils.functions import sendEmbed, sendError


@client.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def roster(ctx, channel: discord.TextChannel, role: discord.Role):
    perms = ctx.message.author.guild_permissions
    tick_emoji = client.get_emoji(806114376297611266)
    redtick_emoji = client.get_emoji(806117763784638464)

    if not perms.administrator:
        await ctx.message.channel.send("**[ERROR]** You must be a server admin in order to create a roster")
        return
    await sendEmbed(
        "Welcome to iBot's Clan Roster Setup\n\nPlease type the header of the roster (top text)\n**Example** My Clan Members",
        "Note: Only use default font, support for different fonts will be added!", ctx)

    def check(m):
        return m.author == ctx.message.author and m.channel == ctx.message.channel

    try:
        msg = await client.wait_for('message', check=check)
    except:
        await sendError("Setup timed out! Please start over.", "", ctx)

    if len(msg.content) > 100:
        await sendError("The header must be less than 100 characters!", "", ctx)
        return
    await msg.add_reaction(tick_emoji)

    clan_emoji = client.get_emoji(812578319308161045)
    await sendEmbed("Please type the clan symbol/emoji: \n**Example** ♅ or {0}".format(clan_emoji), "", ctx)
    try:
        symbol = await client.wait_for('message', timeout=60.0, check=check)
    except:
        await sendError("Setup timed out! Please start over.", "", ctx)

    if len(symbol.content) > 200:
        await sendError("The symbol must be less than 200 characters!", "", ctx)
        return
    await symbol.add_reaction(tick_emoji)

    await sendEmbed("Please type the roster colour RGB:\n**Example** #FF0000", "", ctx)
    try:
        color = await client.wait_for('message', timeout=60.0, check=check)
    except:
        await sendError("Setup timed out! Please start over.", "", ctx)

    await color.add_reaction(tick_emoji)
    try:
        readableHex = await ColourConverter().convert(ctx, color.content)
    except:
        await sendError("Invalid colour code!\nAborting setup.", "", ctx)
        return

    await ctx.message.channel.send("Example of how it will look like:")
    example_msg = '**{0}**\n\n{1} **{2}**'.format(msg.content, symbol.content, "iLearner")
    em = discord.Embed(title='', description=example_msg, colour=readableHex)
    await ctx.message.channel.send(embed=em)
    msg_confirm = await ctx.message.channel.send("React with {0} to confirm!".format(tick_emoji))
    await msg_confirm.add_reaction(tick_emoji)
    await msg_confirm.add_reaction(redtick_emoji)

    def check(reac, reacuser):
        return reacuser == ctx.message.author

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    except:
        await sendError("Setup timed out! Please start over.", "", ctx)
    if reaction.emoji == tick_emoji:
        example_msg = "**{0}**\n\n".format(msg.content)
        for member in ctx.message.channel.guild.members:
            for mrole in member.roles:
                if mrole.id == role.id:
                    if member.nick is not None:
                        example_msg += '{0} **{1}**\n'.format(symbol.content, member.nick)
                    else:
                        example_msg += '{0} **{1}**\n'.format(symbol.content, member.name)

        example_msg += "\n\n"
        if len(example_msg) > 6000:
            await sendError("Members list too long!\n\nSetup aborted!", "", ctx)
            return

        if len(example_msg) > 2000:

            piece = example_msg[1900:2000]
            em = discord.Embed(title='', description=example_msg[:1900 + piece.index("\n")], colour=readableHex)
            msg_id = await channel.send(embed=em)

            st_index = 1900 + piece.index("\n")
            piece = example_msg[3900:4000]
            en_index = 3900 + piece.index("\n")
            em = discord.Embed(title='', description=example_msg[st_index:en_index], colour=readableHex)
            msg_id1 = await channel.send(embed=em)

            if len(example_msg) > 4000:

                piece = example_msg[(len(example_msg) - 100):len(example_msg)]
                st_index = en_index
                en_index = (len(example_msg) - 100) + piece.index("\n")
                em = discord.Embed(title='', description=example_msg[st_index:en_index], colour=readableHex)
                msg_id2 = await channel.send(embed=em)

                added = await add_roster(ctx.message.channel.guild.id, channel.id, role.id,
                                         str(msg_id.id) + "," + str(msg_id1.id) + "," + str(msg_id2.id), msg.content,
                                         symbol.content,
                                         color.content)
            else:
                added = await add_roster(ctx.message.channel.guild.id, channel.id, role.id,
                                         str(msg_id.id) + "," + str(msg_id1.id), msg.content,
                                         symbol.content,
                                         color.content)

        else:
            em = discord.Embed(title='', description=example_msg, colour=readableHex)
            msg_id = await channel.send(embed=em)
            added = await add_roster(ctx.message.channel.guild.id, channel.id, role.id, str(msg_id.id), msg.content,
                                     symbol.content,
                                     color.content)
        if added:
            await sendEmbed("Setup complete!\nUse `irosters` to see the list of rosters", "", ctx)
        else:
            await sendError("Something went wrong...", "", ctx)
            await msg_id.delete()
    else:
        await ctx.message.channel.send("Setup aborted!")


# errors
@roster.error
async def roster_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
        await sendError("**Usage** iroster `#channel` `@role`\n**Example** iroster `#roster` `@myrole`\n\n`Create a roster in your server`", "Make sure you mentione a channel and a role!", ctx)
    elif isinstance(error, asyncio.TimeoutError):
        await sendError("Setup timedout!", "", ctx)
    else:
        await sendError("Something wrong wrong...", "", ctx)



