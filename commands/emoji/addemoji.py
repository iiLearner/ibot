import discord
from discord.ext import commands

from emoji.emoji import save_emoji, Emoji, check_emoji
from main.config import ownerID
from iBot import client
from utils.functions import sendError, sendEmbed


@client.command()
async def addemoji(ctx, member: discord.Member, emoji: discord.Emoji):

    perms = ctx.message.author.guild_permissions
    if ctx.message.author.id != ownerID and not perms.administrator:
        await sendError("You don't have permissions to use this command!", "", ctx)
        return

    if member.bot:
        await sendError("You cannot add emojis to bots!", "", ctx)
        return

    if await check_emoji(member.id, ctx.message.channel.guild.id) and ctx.message.author.id != ownerID:
        await sendError("User already has an emoji!\n\nUse `idelemoji @user` to remove and add again.", "", ctx)
        return

    try:
        await sendEmbed(f"Successfully added {member.mention} to the list with {emoji}", "", ctx)
        await save_emoji(Emoji(emoji.id, member.id, ctx.message.channel.guild.id))
    except:
        await ctx.message.channel.send("Operation failed")


@addemoji.error
async def adduser_error(ctx, error):
    if isinstance(error, commands.EmojiNotFound):
        await sendError(
            f"Failed to add emoji! Make sure the emoji belongs to this server or a server where the bot is present!",
            "", ctx)
    elif isinstance(error, commands.MemberNotFound):
        await sendError(
            f"Failed to find the specified member! make sure the user is in the server!",
            "", ctx)

    elif isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        await sendError("**Usage:** ?iaddemoji `@user\n\nAdd a reaction emoji to a user` `emoji`", "", ctx)
