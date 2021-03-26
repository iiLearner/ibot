import discord
from discord.ext import commands

from iBot import client
from utils.functions import dbConnect, sendError, escape_string


@client.command(aliases=["close_tourney"])
@commands.cooldown(1, 30, commands.BucketType.user)
async def cancel_tourney(ctx):
    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute("SELECT * FROM tournaments WHERE userid = " + str(ctx.message.author.id) + " AND status = 1")
    result = mycursor.fetchone()
    if result is None:
        await ctx.message.channel.send("**[ERROR]** You don't have a tourney! Create one with `icreate_tourney`!")
        return
    else:
        try:
            logs_channel = client.get_channel(int(result[4]))
            alerts_channel = client.get_channel(int(result[5]))
            category_channel = logs_channel.category
            await logs_channel.delete()
            await alerts_channel.delete()
            await category_channel.delete()
        except:
            await ctx.message.channel.send("**[Warning]** I was unable to delete the anticheat channels! (missing permissions or channels?)")

        mycursor.execute("UPDATE tournaments SET status = 0 WHERE userid = " + str(ctx.message.author.id) + "")
        con.commit()
        await ctx.message.channel.send(
            "**[SUCCESS]** Tournament has been cancelled! Create a new one with `?create_tourney`!")
        con.close()


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def create_tourney(ctx, *, name=None):

    if name is None:
        await ctx.message.channel.send("**Usage:** icreate_tourney `<name>`")
        return

    try:
        perms = ctx.message.author.guild_permissions
        if not perms.administrator:
            await sendError("You must be a server admin in order to create a tournament!",  "", ctx)
            return

        myperms = ctx.message.channel.guild.me.guild_permissions
        if not myperms.manage_channels:
            await sendError("I need manage channel permission in order to do this!", "", ctx)
            return

        name = name.replace("<", "").replace(">", "")

        con = await dbConnect()
        mycursor = con.cursor()
        mycursor.execute(f"SELECT * FROM tournaments WHERE userid = {ctx.message.author.id} AND status = 1")
        result = mycursor.fetchone()
        if result is not None:
            await ctx.message.channel.send(
                "**[ERROR]** You already have an ongoing tournament! cancel it first using `icancel_tourney`!")
            return

        await ctx.trigger_typing()

        category = await ctx.message.channel.guild.me.guild.create_category(name)
        overwrites = {
            ctx.message.channel.guild.me.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.message.channel.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            ctx.message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        logs = await ctx.message.channel.guild.me.guild.create_text_channel("┌📈𝗟𝗢𝗚𝗦", overwrites=overwrites, category=category)
        alerts = await ctx.message.channel.guild.me.guild.create_text_channel("└👥𝗔𝗟𝗘𝗥𝗧𝗦", overwrites=overwrites, category=category)

        av_commands = "Here's the list of available commands that can be used in {0} or {1} by organizers!\n`closeconnection name` - Close the connection for a" \
                      "user.\n**Example:** `closeconnection iLearner`\n\n`processlist name` - Get the current list of running processes from task manager for a " \
                      "user.\n**Example:**`processlist iLearner`\n\nHope you enjoy your time!".format(logs.mention,
                                                                                                      alerts.mention)
        em = discord.Embed(title='Available commands', description=av_commands, colour=0x2ecc71)
        em.set_author(name='', icon_url=ctx.message.author.avatar_url)
        em.set_footer(text=name, icon_url=ctx.message.channel.guild.me.avatar_url)
        await logs.send(embed=em)
        await alerts.send(embed=em)

        myemoji = client.get_emoji(787237116630532106)
        chemoji = client.get_emoji(788129603876421632)
        msg = '┌─────┈{0}┈────┐\n{6}Tournament created!{7}\n└─────┈{1}┈────┘\n\nTournament has been created!\n\nTournament name: {2}\nTournament organizer: {3}\nLogs channel: {4}\nAlerts channel: {5}\n\nPlease add members to your tournament with the command `itourney_role @role`\n\nSend private keys to all members before the tournament with the command `isendkeys`'.format(
            myemoji, myemoji, name, ctx.message.author.mention, logs.mention, alerts.mention, chemoji, chemoji)
        em = discord.Embed(title='', description=msg, colour=0x9b59b6)
        em.set_author(name='', icon_url=ctx.message.author.avatar_url)
        em.set_footer(text="Tournament created!", icon_url=ctx.message.channel.guild.me.avatar_url)
        await ctx.message.channel.send(embed=em)

        query = f"INSERT INTO tournaments (name, userid, serverid, logchannel, alertchannel) VALUES ('{escape_string(name)}', '{ctx.message.author.id}', '{ctx.message.channel.guild.me.guild.id}', '{logs.id}', '{alerts.id}')"
        mycursor.execute(query)
        con.commit()
        con.close()
    except Exception as e:
        await sendError(f"Something went wrong... contant admin!\nPlease report the following error log:`\n{str(e)}", "", ctx)
