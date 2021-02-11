import uuid
import discord

from iBot import client
from utils.functions import dbConnect


@client.command()
async def cleanerkey(ctx, userid: int):
    if ctx.message.author.id != 266947686194741248:
        await ctx.message.channel.send("no")
        return
    me = ctx.message.channel.guild.me
    tosend = client.get_user(userid)

    myemoji = client.get_emoji(787237116630532106)
    chemoji = client.get_emoji(788129603876421632)
    key = uuid.uuid1()
    msg = '┌─────┈{0}┈────┐\n{3}Clearner Key!{4}\n└─────┈{1}┈────┘\n\nCleaner key has been generated!\n\n\nPrivate ' \
          'key: `{2}`\n\nPlease use this key log into the cleaner client!'.format(
        myemoji, myemoji, key, chemoji, chemoji)
    em = discord.Embed(title='', description=msg, colour=0x9b59b6)
    em.set_author(name='', icon_url=ctx.message.author.avatar_url)
    em.set_footer(text="Key generated!", icon_url=me.avatar_url)
    try:
        await tosend.send(embed=em)
    except:
        await ctx.message.channel.send(
            "I could not send the code to " + tosend.name + tosend.discriminator + ". Kindly ask them to change their "
                                                                                   "dm settings and try again!")

    con = await dbConnect()
    mycursor = con.cursor()
    mycursor.execute("INSERT INTO clean (mkey, userid) VALUES ('" + str(key) + "', '" + str(tosend.id) + "')")
    con.commit()
    con.close()
    await ctx.message.channel.send("Keys has successfully been sent!")
