from emoji.emoji import load_emojis
from iBot import client
from mute.mute import loadMutes
from roster.roster import check_rosters


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await loadMutes()
    await load_emojis()
    await check_rosters()
