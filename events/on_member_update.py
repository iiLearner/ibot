import discord

from iBot import client, roster_list
from roster.roster import Roster, del_roster, loadrosters, check_rosters
from utils.functions import dbConnect


async def isRosterGuild(guild: discord.Guild):
    for x in roster_list:
        if x.server == guild.id:
            return True
    return False


async def isRosterRole(before, after):
    roles = [x for x in before.roles if x not in after.roles]
    if len(roles) == 0:
        roles = [x for x in after.roles if x not in before.roles]
    for x in roster_list:
        if x.role == roles[0].id:
            return x
    return False


async def update_roster(roster: Roster):
    checkMore = False
    channel = client.get_channel(roster.channel)
    if channel is None:
        await del_roster(roster.id)
        return
    try:
        messages = roster.msg_id.split(",")
        message = await channel.fetch_message(int(messages[0]))
        try:
            message1 = await channel.fetch_message(int(messages[1]))
            message2 = await channel.fetch_message(int(messages[2]))
            checkMore = True
        except:
            pass

        example_msg = "**{0}**\n\n".format(roster.header)
        readableHex = int(hex(int(roster.colour.replace("#", ""), 16)), 0)
        for member in message.channel.guild.members:
            for mrole in member.roles:
                if mrole.id == roster.role:
                    if member.nick is not None:
                        example_msg += '{0} **{1}**\n'.format(roster.symbol, member.nick)
                    else:
                        example_msg += '{0} **{1}**\n'.format(roster.symbol, member.name)

        example_msg += "\n\n"
        if checkMore:
            if len(example_msg) > 2000:
                piece = example_msg[1900:2000]
                em = discord.Embed(title='', description=example_msg[:1900 + piece.index("\n")], colour=readableHex)
                await message.edit(embed=em)

                st_index = 1900 + piece.index("\n")
                piece = example_msg[3900:4000]
                en_index = 3900 + piece.index("\n")
                em = discord.Embed(title='', description=example_msg[st_index:en_index], colour=readableHex)
                await message1.edit(embed=em)

                if len(example_msg) > 4000:

                    piece = example_msg[(len(example_msg) - 100):len(example_msg)]
                    st_index = en_index
                    en_index = (len(example_msg) - 100) + piece.index("\n")
                    em = discord.Embed(title='', description=example_msg[st_index:en_index], colour=readableHex)
                    await message2.edit(embed=em)

            else:
                em = discord.Embed(title='', description=example_msg, colour=readableHex)
                await message.edit(embed=em)
        else:
            em = discord.Embed(title='', description=example_msg, colour=readableHex)
            await message.edit(embed=em)

    except:
        await check_rosters()


@client.event
async def on_member_update(before, after):
    # make sure the updated member belongs to a guild that has an active roster
    if await isRosterGuild(before.guild):

        # make sure roles have changed
        if len(before.roles) != len(after.roles):

            # the role updated was a roster role
            roster = await isRosterRole(before, after)
            if not not roster:
                await update_roster(roster)
