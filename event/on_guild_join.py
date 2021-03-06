from main.config import ownerID
from iBot import client
from utils.functions import getWelcomeChannel, sendHelpMessage


@client.event
async def on_guild_join(guild):
    me = client.get_user(ownerID)
    await me.send("I just joined the guild: " + guild.name + "")

    channel = await getWelcomeChannel(guild)
    try:
        await sendHelpMessage(channel)
    except:
        pass
