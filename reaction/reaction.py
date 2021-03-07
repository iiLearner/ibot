import time


class ReactionTime:
    def __init__(self, userid, timestamp):
        self.userid = userid
        self.timestamp = timestamp


last_reaction = []


def setReactionTime(userid: int, timestamp: int):
    for x in last_reaction:
        if x.userid == userid:
            x.timestamp = timestamp
            return True
    last_reaction.append(ReactionTime(userid, timestamp))


async def getReactionTime(userid: int):
    for x in last_reaction:
        if x.userid == userid:
            return x.timestamp
    last_reaction.append(ReactionTime(userid, int(time.time()-10)))
    return int(time.time()-10)
