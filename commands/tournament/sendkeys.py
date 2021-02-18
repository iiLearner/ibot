import uuid
import discord
from iBot import client
from utils.functions import dbConnect
from utils.tournaments.functions import codeSent


@client.command()
async def sendkeys(ctx):
    me = ctx.message.channel.guild.me

    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute("SELECT * FROM tournaments WHERE userid = " + str(ctx.message.author.id) + " and status = 1")
    result = mycursor.fetchone()
    if result is None:
        await ctx.message.channel.send("**[ERROR]** You don't have a tourney! Create one with `?create_tourney`!")
        return

    if result[7] is None:
        await ctx.message.channel.send(
            "**[ERROR]** You must link a role to the tourney first! Link one with `?tourney_role`!")
        return

    progress = await ctx.message.channel.send("Sending keys...")

    mycursor.execute(
        "SELECT * FROM tournaments WHERE userid = " + str(ctx.message.author.id) + " AND status = 1 LIMIT 1")
    tournament_info = mycursor.fetchone()

    mycursor.execute("SELECT * FROM players WHERE tID = " + str(tournament_info[0]) + " and codeStatus = 1")
    player_info = mycursor.fetchall()

    count = 0
    for member in me.guild.members:
        for role in member.roles:
            if role.id == int(tournament_info[7]):

                mycursor.execute("SELECT * FROM players WHERE userid = '" + str(member.id) + "' AND tID = " + str(
                    tournament_info[0]) + " LIMIT 1")
                u_info = mycursor.fetchone()
                if u_info is None:
                    mycursor.execute(
                        "INSERT INTO players (tID, userid) VALUES ('" + str(tournament_info[0]) + "', '" + str(
                            member.id) + "')")
                    con.commit()

                if not codeSent(player_info, member.id):

                    myemoji = client.get_emoji(787237116630532106)
                    chemoji = client.get_emoji(788129603876421632)
                    userobj = client.get_user(int(tournament_info[2]))
                    key = uuid.uuid1()
                    msg = '┌─────┈{0}┈────┐\n{5}Tournament Keys!{6}\n└─────┈{1}┈────┘\n\nTournament key has been generated!\n\nTournament name: {2}\nTournament organizer: {3}\nPrivate key: `{4}`\n\nPlease use this key log into the anticheat client!'.format(
                        myemoji, myemoji, tournament_info[1], userobj.name, key, chemoji, chemoji)
                    em = discord.Embed(title='', description=msg, colour=0x9b59b6)
                    em.set_author(name='', icon_url=ctx.message.author.avatar_url)
                    em.set_footer(text="Key generated!", icon_url=me.avatar_url)
                    try:
                        await member.send(embed=em)
                        await member.send(
                            "Join the support server to download the client: https://discord.gg/79kbdEDwnV")
                        mycursor.execute(
                            "UPDATE players SET code = '" + str(key) + "', codeStatus = 1 WHERE userid = '" + str(
                                member.id) + "' AND tID = '" + str(tournament_info[0]) + "'")
                        con.commit()
                        count += 1
                        await progress.edit(content="Sent keys to: {0} | Total keys send: {1}".format(member.name, count))
                    except:
                        await ctx.message.channel.send(
                            "I could not send the code to " + member.name + member.discriminator + ". Kindly ask them to change their dm settings and use `?sendkeys` again!")

    await progress.edit(content="Keys have successfully been sent to " + str(count) + " user(s)!")
    con.close()
