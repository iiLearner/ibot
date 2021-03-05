from main.config import ownerID
from iBot import client


@client.event
async def on_guild_remove(guild):
    me = client.get_user(ownerID)
    await me.send("I just left the guild: " + guild.name + "")
