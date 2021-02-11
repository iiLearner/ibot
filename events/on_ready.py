from emojis import emoji

from iBot import client
from roster.roster import loadrosters, check_rosters


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await emoji.load_emojis()
    await loadrosters()
    await check_rosters()



