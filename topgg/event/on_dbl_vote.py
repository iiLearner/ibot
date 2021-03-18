from iBot import client
from main.config import ownerID


@client.event
async def on_dbl_vote(data):
    owner = client.get_user(ownerID)
    await owner.send(data)
