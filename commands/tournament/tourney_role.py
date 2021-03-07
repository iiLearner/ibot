from discord.ext import commands

from iBot import client
from utils.functions import dbConnect
from utils.tournaments.functions import roleExists


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def tourney_role(ctx, roleidEx=None):
    if roleidEx is None:
        await ctx.message.channel.send("**Usage:** ?tourney_role `@role`")
        return

    check = roleidEx.isnumeric()
    await ctx.trigger_typing()
    if check:
        roleid = roleidEx
    else:
        mrole = roleidEx.replace("<@&", "").replace(">", "").replace("<@!", "")
        frole = ctx.message.channel.guild.get_role(int(mrole))
        if hasattr(frole, 'id'):
            roleid = frole.id
        else:
            roleid = 12342342323434

    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute("SELECT * FROM tournaments WHERE userid = " + str(ctx.message.author.id) + " and status = 1")
    result = mycursor.fetchone()
    if result is None:
        await ctx.message.channel.send("**[ERROR]** You don't have a tourney! Create one with `?create_tourney`!")
        return

    me = ctx.message.channel.guild.me
    if roleExists(roleid, me.guild):
        mrole = me.guild.get_role(int(roleid))
        await ctx.message.channel.send(
            "**[SUCCESS]** Role " + mrole.name + " has been linked with your tourney! Send keys before the tournament with `?sendkeys`")
        mycursor.execute("UPDATE tournaments SET roleid = " + str(roleid) + " WHERE ID = " + str(result[0]) + "")
        con.commit()
    else:
        await ctx.message.channel.send("**[ERROR]** Role not found!")

    con.close()
