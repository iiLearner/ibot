import discord
from iBot import client
from utils.functions import dbConnect


@client.command()
async def cancel_tourney(ctx):
    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute("SELECT * FROM tournaments WHERE userid = " + str(ctx.message.author.id) + " AND status = 1")
    result = mycursor.fetchone()
    if result is None:
        await ctx.message.channel.send("**[ERROR]** You don't have a tourney! Create one with `?create_tourney`!")
        return
    else:
        logs_channel = client.get_channel(int(result[4]))
        alerts_channel = client.get_channel(int(result[5]))
        category_channel = logs_channel.category

        await logs_channel.delete()
        await alerts_channel.delete()
        await category_channel.delete()

        mycursor.execute("UPDATE tournaments SET status = 0 WHERE userid = " + str(ctx.message.author.id) + "")
        con.commit()
        await ctx.message.channel.send(
            "**[SUCCESS]** Tournament has been cancelled! Create a new one with `?create_tourney`!")
        con.close()


@client.command()
async def create_tourney(ctx, *, name=None):
    if name is None:
        await ctx.message.channel.send("**Usage:** ?create_tourney <name>")
        return

    perms = ctx.message.author.guild_permissions
    if not perms.administrator:
        await ctx.message.channel.send("**[ERROR]** You must be a server admin in order to create a tournament!")
        return
    name = name.replace("<", "").replace(">", "")

    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute("SELECT * FROM tournaments WHERE userid = " + str(ctx.message.author.id) + " and status = 1")
    result = mycursor.fetchone()
    if result is not None:
        await ctx.message.channel.send(
            "**[ERROR]** You already have an ongoing tournament! cancel it first using `?cancel_tourney`!")
        return

    await ctx.trigger_typing()
    me = ctx.message.channel.guild.me
    permissions = me.guild_permissions
    if permissions.manage_channels:
        pass
    else:
        await ctx.message.channel.send("**Error!** I do not have permissions to create channels!")

    category = await me.guild.create_category("AntiCheat")
    overwrites = {
        me.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        ctx.message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    logs = await me.guild.create_text_channel("┌📈𝗟𝗢𝗚𝗦", overwrites=overwrites, category=category)
    alerts = await me.guild.create_text_channel("└👥𝗔𝗟𝗘𝗥𝗧𝗦", overwrites=overwrites, category=category)

    av_commands = "Here's the list of available commands that can be used in {0} or {1} by organizers!\n`closeconnection name` - Close the connection for a" \
                  "user.\n**Example:** `closeconnection iLearner`\n\n`processlist name` - Get the current list of running processes from task manager for a " \
                  "user.\n**Example:**`processlist iLearner`\n\nHope you enjoy your time!".format(logs.mention,
                                                                                                  alerts.mention)
    em = discord.Embed(title='Available commands', description=av_commands, colour=0x2ecc71)
    em.set_author(name='', icon_url=ctx.message.author.avatar_url)
    em.set_footer(text=name, icon_url=me.avatar_url)
    await logs.send(embed=em)
    await alerts.send(embed=em)

    myemoji = client.get_emoji(787237116630532106)
    chemoji = client.get_emoji(788129603876421632)
    msg = '┌─────┈{0}┈────┐\n{6}Tournament created!{7}\n└─────┈{1}┈────┘\n\nTournament has been created!\n\nTournament name: {2}\nTournament organizer: {3}\nLogs channel: {4}\nAlerts channel: {5}\n\nPlease add members to your tournament with the command `?tourney_role @role`\n\nSend private keys to all members before the tournament with the command `?sendkeys`'.format(
        myemoji, myemoji, name, ctx.message.author.mention, logs.mention, alerts.mention, chemoji, chemoji)
    em = discord.Embed(title='', description=msg, colour=0x9b59b6)
    em.set_author(name='', icon_url=ctx.message.author.avatar_url)
    em.set_footer(text="Tournament created!", icon_url=me.avatar_url)
    await ctx.message.channel.send(embed=em)

    query = "INSERT INTO tournaments (name, userid, serverid, logchannel, alertchannel) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(
        name, ctx.message.author.id, me.guild.id, logs.id, alerts.id)
    mycursor.execute(query)
    con.commit()
    con.close()
