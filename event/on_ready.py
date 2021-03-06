from emoji import emoji
from iBot import client
from roster.roster import check_rosters
from utils.functions import getWelcomeChannel


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await emoji.load_emojis()
    await check_rosters()
