from emoji.emoji import load_emojis
from iBot import client
from mute.mute import loadMutes
from roster.roster import check_rosters
from topgg.init import dbl_init
from topgg.event import on_dbl_vote


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await loadMutes()
    await load_emojis()
    await check_rosters()
    dbl_client = dbl_init(client)
    await dbl_client.post_guild_count()


