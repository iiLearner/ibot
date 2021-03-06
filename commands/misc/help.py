import discord
from discord.ext import commands

from iBot import client
from utils.functions import sendCooldown, sendHelpMessage


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def help(ctx):
    await sendHelpMessage(ctx.message.channel)


@help.error
async def help_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await sendCooldown(error.retry_after, ctx)
