import discord

from iBot import muted_list
from utils.functions import dbConnect


class Mute:
    def __init__(self, user, server, flag):
        self.user = user
        self.server = server
        self.flag = flag


async def loadMutes():
    count = 0
    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute("SELECT userid, serverid FROM mute")
    results = mycursor.fetchall()
    for x in results:
        muted_list.append(Mute(int(x[0]), int(x[1]), 0))
        count += 1
    print(f"Successfully loaded {count} mutes!")
    con.close()


async def addMute(user: int, server: int, flag):
    # add local mute
    muted_list.append(Mute(user, server, flag))
    # add db mute
    query = f"INSERT INTO mute (userid, serverid) VALUES ('{user}', '{server}')"
    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute(query)
    con.commit()
    con.close()


async def delMute(user: int, server: int):
    for x in muted_list:
        if x.user == user and x.server == server:
            # remove locally
            muted_list.remove(x)
            # remove from db
            query = f"DELETE FROM mute WHERE userid = {user} AND serverid = {server}"
            con = await dbConnect()
            mycursor = con.cursor()
            mycursor.execute(query)
            con.commit()
            con.close()


async def isMuted(userid: int, serverid: int):
    for x in muted_list:
        if x.user == userid and x.server == serverid:
            return True
    return False
