from discord.ext import commands

from iBot import client
from main.config import ownerID
from utils.functions import sendCooldown


@client.event
async def on_command_error(ctx, error):

    # cool down message
    if isinstance(error, commands.CommandOnCooldown):
        await sendCooldown(error.retry_after, ctx)

    # avoid annoying console logs
    if isinstance(error, commands.CommandNotFound):
        pass

    else:
        owner = client.get_user(ownerID)
        await owner.send(error)
