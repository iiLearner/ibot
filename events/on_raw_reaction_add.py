import discord
from iBot import client


@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 810289926007947274:
        role = client.get_guild(payload.guild_id).get_role(810455753881026590)
        await payload.member.add_roles(role)
        msg = "Thank you for agreeing to the selfish wonderer tournament rules!\nFor any further questions do no hesitate contacting the host!"
        em = discord.Embed(title='Rules read', description=msg, colour=0x9b59b6)
        em.set_author(name='', icon_url=payload.member.avatar_url)
        await payload.member.send(embed=em)
