from iBot import client
import iBot
import discord

from main.config import ownerID
from utils.functions import dbConnect


@client.command()
async def tlist(ctx):
    if ctx.message.author.id != ownerID:
        await ctx.message.channel.send("no")
    con = await dbConnect()
    iBot.mycursor = con.cursor()

    iBot.mycursor.execute("SELECT * FROM tournaments WHERE  status = 1")
    result = iBot.mycursor.fetchall()

    msg = ""
    for x in result:
        try:
            user = client.get_user(int(x[2]))
            guild = client.get_guild(int(x[3]))
            msg += "`ID` **{0}** | `Name` **{1}** | `User` **{2}** | `Server` **{3}**\n".format(x[0], x[1],
                                                                                                user.name,
                                                                                                guild.name)
        except:
            continue

    if len(result) == 0:
        msg = "No tournaments available for this server\n"

    em = discord.Embed(title='', description=msg, colour=0xe67e22)
    em.set_footer(text="", icon_url=ctx.message.channel.guild.icon_url)
    await ctx.message.channel.send(embed=em)
    con.close()
