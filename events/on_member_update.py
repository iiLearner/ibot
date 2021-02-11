import discord

from iBot import client, roster_list
from roster.roster import Roster, del_roster, loadrosters
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

    channel = client.get_channel(roster.channel)
    if channel is None:
        await del_roster(roster.id)
        return
    try:
        message = await channel.fetch_message(roster.msg_id)
        example_msg = "**{0}**\n\n".format(roster.header)
        readableHex = int(hex(int(roster.colour.replace("#", ""), 16)), 0)
        for member in message.channel.guild.members:
            for mrole in member.roles:
                if mrole.id == roster.role:
                    example_msg += '{0} **{1}**\n'.format(roster.symbol, member.name)
        example_msg += "\n\n"
        em = discord.Embed(title='', description=example_msg, colour=readableHex)
        await message.edit(embed=em)

    except:
        example_msg = "**{0}**\n\n".format(roster.header)
        readableHex = int(hex(int(roster.colour.replace("#", ""), 16)), 0)
        for member in channel.guild.members:
            for mrole in member.roles:
                if mrole.id == roster.role:
                    example_msg += '{0} **{1}**\n'.format(roster.symbol, member.name)
        example_msg += "\n\n"
        em = discord.Embed(title='', description=example_msg, colour=readableHex)
        msg = await channel.send(embed=em)
        query = 'UPDATE roster SET messageid = {0} WHERE ID = {1}'.format(msg.id, roster.id)
        con = await dbConnect()
        mycursor = con.cursor()
        mycursor.execute(query)
        con.commit()
        con.close()

        roster_list.clear()
        await loadrosters()


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
