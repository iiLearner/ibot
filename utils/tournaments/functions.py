def codeSent(player_info, userid):
    toReturn = False
    for x in player_info:
        if int(x[2]) == userid:
            toReturn = True
            break
    return toReturn


def roleExists(roleid, guild):
    toReturn = False
    for role in guild.roles:
        if role.id == int(roleid):
            toReturn = True
            break
    return toReturn