import discord

from iBot import muted_list


class Mute:
    def __init__(self, user, server, flag):
        self.user = user
        self.server = server
        self.flag = flag


async def addMute(user: int, server: int, flag):
    muted_list.append(Mute(user, server, flag))


async def delMute(user: int):
    for x in muted_list:
        if x.user == user:
            muted_list.remove(x)
