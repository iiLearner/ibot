import discord
from discord.ext import commands

from iBot import client


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def help(ctx):

    message = "Here is the list of commands!\nFor more info on a command, use `{command}` to view usage help.\nFor further assistance join our [guild](https://discord.gg/79kbdEDwnV)\n\n"
    em = discord.Embed(title='', description=message, colour=0xe67e22)
    em.set_author(name="Command help", icon_url=ctx.message.channel.guild.icon_url)

    emoji = client.get_emoji(788351325531537428)
    em.add_field(name=f"{emoji} Emoji", value="`addemoji` `delemoji`", inline=False)

    emoji = client.get_emoji(777915907644850227)
    em.add_field(name=f"{emoji} Roster", value="`roster` `droster` `rosters`", inline=False)

    emoji = client.get_emoji(817499208189345882)
    em.add_field(name=f"{emoji} Tournament", value="`create_tourney` `cancel_tourney` `tourney_role` `sendkeys` `close_tourney`", inline=False)

    emoji = client.get_emoji(565838171363868682)
    em.add_field(name=f"{emoji} Special Mute", value="`mute` `unmute`", inline=False)

    emoji = client.get_emoji(817523844004053044)
    em.add_field(name=f"{emoji} Minecraft", value="`server`", inline=False)

    em.set_footer(text="You must use `i` prefix before the commands!", icon_url=client.user.avatar_url)
    await ctx.message.channel.send(embed=em)
