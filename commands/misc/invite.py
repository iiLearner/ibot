from discord.ext import commands

from iBot import client
from utils.functions import sendCooldown, sendEmbed


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def invite(ctx):
    await sendEmbed("Click [here](https://discord.com/oauth2/authorize?client_id=379624030317182976&permissions=11344&scope=bot) to invite me!", "", ctx)


@invite.error
async def invite_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await sendCooldown(error.retry_after, ctx)