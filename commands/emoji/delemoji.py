import discord
from discord.ext import commands
from emoji.emoji import delete_emoji, check_emoji, delete_user_emoji
from main.config import ownerID
from iBot import client
from utils.functions import sendEmbed, sendError


@client.command()
async def delemoji(ctx, member: discord.Member, emoji=None):
    perms = ctx.message.author.guild_permissions
    if ctx.message.author.id != ownerID and not perms.administrator:
        await sendError("You don't have permissions to use this command!", "", ctx)
        return
    if not await check_emoji(member.id, ctx.message.channel.guild.id) and ctx.message.author.id != ownerID:
        await sendError("User has no emoji set!\n\nUse `iaddemoji @user :emoji:` to remove and add again.", "", ctx)
        return

    try:
        if emoji is not None:
            await delete_emoji(emoji.id, member.id, ctx.message.channel.guild.id)
        else:
            await delete_user_emoji(member.id, ctx.message.channel.guild.id)
        await sendEmbed(f"Successfully removed {member.mention}'s emoji from the list!", "", ctx)
    except:
        await ctx.message.channel.send("Operation failed")


@delemoji.error
async def delemoji_error(ctx, error):
    if isinstance(error, commands.EmojiNotFound):
        await sendError(
            f"Failed to add emoji! Make sure the emoji belongs to this server or a server where the bot is present!",
            "", ctx)
    elif isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.MemberNotFound):
        await sendError("**Usage:** ?idelemoji `@user`", "", ctx)