from main.config import ownerID
from iBot import client
from utils.functions import getWelcomeChannel, sendWelcomeMessage


@client.event
async def on_guild_join(guild):
    me = client.get_user(ownerID)
    await me.send("I just joined the guild: " + guild.name + "")

    channel = await getWelcomeChannel(guild)
    try:
        await sendWelcomeMessage(channel)
    except:
        pass
