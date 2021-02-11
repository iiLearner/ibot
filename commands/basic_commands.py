import discord
from main.config import ownerID
from iBot import client
import os


@client.command()
async def spam_dm(ctx, mem: discord.Member, number: int, *, mystring: str):
    if ctx.message.author.id == ownerID:
        current = 0
        emoji = '\U0001F44D'
        await ctx.message.add_reaction(emoji)
        while current < number:
            try:
                current = current + 1
                await mem.send(mystring)
            except:
                await ctx.message.channel.send("Unable to dm this thing..")
                break


@client.command()
async def set_status(ctx, *, mystring: str):
    if ctx.message.author.id == ownerID:
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=mystring))
        emoji = '\U0001F44D'
        await ctx.message.add_reaction(emoji)


@client.command()
async def offline(ctx):
    if ctx.message.author.id == ownerID:
        emoji = '\U0001F44D'
        await ctx.message.add_reaction(emoji)
        await client.close()


@client.command()
async def reboot(ctx):
    if ctx.message.author.id == ownerID:
        emoji = '\U0001F44D'
        await ctx.message.add_reaction(emoji)
        os.system("service ibot restart")


@client.command()
async def command(ctx, *, cmd):
    if ctx.message.author.id == ownerID:
        emoji = '\U0001F44D'
        await ctx.message.add_reaction(emoji)
        os.system(cmd)

