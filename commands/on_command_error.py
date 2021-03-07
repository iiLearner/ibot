from discord.ext import commands

from iBot import client
from utils.functions import sendCooldown


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await sendCooldown(error.retry_after, ctx)
    if isinstance(error, commands.CommandNotFound):
        pass
