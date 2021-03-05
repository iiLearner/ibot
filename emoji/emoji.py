import iBot
from iBot import emoji_list
from utils.functions import dbConnect


class Emoji:
    def __init__(self, emojiid, userid, serverid):
        self.emoji = emojiid
        self.user = userid
        self.server = serverid


async def load_emojis():
    count = 0
    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute("SELECT emoji, user, server FROM emoji")
    results = mycursor.fetchall()
    for x in results:
        emoji_list.append(Emoji(int(x[0]), int(x[1]), int(x[2])))
        count += 1
    print("Successfully loaded {0} emojis!".format(count))
    con.close()


async def check_emoji(user: int, server: int):

    for emoji in emoji_list:
        if emoji.user == user and emoji.server == server:
            return True
    return False


async def save_emoji(emoji: Emoji):

    emoji_list.append(emoji)
    query = "INSERT INTO emoji (emoji, user, server) VALUES ('{0}', '{1}', '{2}')".format(emoji.emoji, emoji.user,
                                                                                          emoji.server)
    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute(query)
    con.commit()
    con.close()


async def delete_emoji(emojiid: int, userid: int, serverid: int):
    for x in emoji_list:
        if userid == x.user and serverid == x.server and emojiid == x.emoji:
            emoji_list.remove(x)
            break
    query = "DELETE FROM emoji WHERE emoji = {0} AND user = {1} AND server = {2}".format(emojiid, userid, serverid)
    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute(query)
    con.commit()
    con.close()


async def delete_user_emoji(userid: int, serverid: int):
    for x in emoji_list:
        if userid == x.user and serverid == x.server:
            emoji_list.remove(x)

    query = "DELETE FROM emoji WHERE user = {0} AND server = {1}".format(userid, serverid)
    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute(query)
    con.commit()
    con.close()
