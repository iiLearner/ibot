import discord

import iBot
from iBot import roster_list
from utils.functions import dbConnect


class Roster:
    def __init__(self, id, server, channel, role, msg, header, symbol, colour):
        self.id = id
        self.server = server
        self.channel = channel
        self.role = role
        self.msg_id = msg
        self.header = header
        self.symbol = symbol
        self.colour = colour


async def loadrosters():
    count = 0
    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute("SELECT * FROM roster WHERE soft_deleted = 0 ORDER BY ID")
    results = mycursor.fetchall()

    for x in results:
        count += 1
        roster_list.append(Roster(int(x[0]), int(x[1]), int(x[2]), int(x[3]), x[4], x[5], x[6], x[7]))
    print("Successfully loaded {0} rosters!".format(count))
    con.close()


async def rosterlist(server: int):
    return_list = []
    for x in roster_list:
        if x.server == server:
            return_list.append(x)
    return return_list


async def add_roster(server: int, channel: int, role: int, msg: str, header: str, symbol: str, colour: str):
    try:
        # insert db
        query = 'INSERT INTO roster (serverid, channelid, roleid, messageid, header, symbol, colour) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}","{5}", "{6}")'.format(
            server, channel, role, msg, header, symbol, colour)
        con = await dbConnect()
        mycursor = con.cursor()
        mycursor.execute(query)
        con.commit()

        # get last inserted ID
        query = "SELECT ID FROM roster ORDER BY ID DESC LIMIT 1"
        mycursor.execute(query)
        result_id = mycursor.fetchone()
        con.close()

        # add to local
        roster_list.append(Roster(result_id[0], server, channel, role, msg, header, symbol, colour))
        return True
    except:
       return False


async def check_rosters():
    for x in roster_list:

        channel = iBot.client.get_channel(x.channel)
        if channel is None:
            await del_roster(x.id)
            continue
        try:
            messages = x.msg_id.split(",")
            for msgid in messages:
                await channel.fetch_message(int(msgid))
        except:
            try:
                messages = x.msg_id.split(",")
                for msgid in messages:
                    message = await channel.fetch_message(int(msgid))
                    await message.delete()
            except:
                pass

            example_msg = "**{0}**\n\n".format(x.header)
            readableHex = int(hex(int(x.colour.replace("#", ""), 16)), 0)
            for member in channel.guild.members:
                for mrole in member.roles:
                    if mrole.id == x.role:
                        if member.nick is not None:
                            example_msg += '{0} **{1}**\n'.format(x.symbol, member.nick)
                        else:
                            example_msg += '{0} **{1}**\n'.format(x.symbol, member.name)
            example_msg += "\n\n"

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

                    piece = example_msg[(len(example_msg)-100):len(example_msg)]
                    st_index = en_index
                    en_index = (len(example_msg)-100) + piece.index("\n")
                    em = discord.Embed(title='', description=example_msg[st_index:en_index], colour=readableHex)
                    msg_id2 = await channel.send(embed=em)
                    query = 'UPDATE roster SET messageid = "{0}" WHERE ID = {1}'.format(str(msg_id.id)+","+str(msg_id1.id)+","+str(msg_id2.id), x.id)

                else:
                    query = 'UPDATE roster SET messageid = "{0}" WHERE ID = {1}'.format(str(msg_id.id)+","+str(msg_id1.id), x.id)

            else:
                em = discord.Embed(title='', description=example_msg, colour=readableHex)
                msg_id = await channel.send(embed=em)
                query = 'UPDATE roster SET messageid = "{0}" WHERE ID = {1}'.format(str(msg_id.id), x.id)

            con = await dbConnect()
            mycursor = con.cursor()
            mycursor.execute(query)
            con.commit()
            con.close()
            roster_list.clear()
    await loadrosters()


async def del_roster(roster_id: int):

    query = "SELECT * FROM roster WHERE ID = {0}".format(roster_id)
    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute(query)
    result = mycursor.fetchone()
    if result is None:
        return False

    try:
        for x in roster_list:
            if x.server == int(result[1]) and x.channel == int(result[2]) and x.id == int(result[0]):
                roster_list.remove(x)
                try:
                    channel = iBot.client.get_channel(x.channel)
                    messages = x.msg_id.split(",")
                    for msgid in messages:
                        message = await channel.fetch_message(int(msgid))
                        await message.delete()
                except:
                    pass
                break

        query = "UPDATE roster SET soft_deleted = 1 WHERE ID = {0}".format(result[0])
        mycursor.execute(query)
        con.commit()
        con.close()
        return True

    except:
        return False
