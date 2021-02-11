import random

import discord

from iBot import client, emoji_list, muted_list
from strings.quotes import quotes, answers


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    for x in muted_list:
        if x.user == message.author.id:
            if x.flag == 1:
                try:
                    await message.delete()
                except:
                    continue
            else:
                if x.server == message.channel.guild.id:
                    try:
                        await message.delete()
                    except:
                        continue

    if not isinstance(message.channel, discord.abc.PrivateChannel):
        for x in emoji_list:
            if message.channel.guild.id == x.server and message.author.id == x.user:
                emoji = client.get_emoji(x.emoji)
                await message.add_reaction(emoji)

    if isinstance(message.channel, discord.abc.PrivateChannel):
        item = random.choice(quotes)
        await message.channel.send(item)

    if (
            "cj" in message.content.lower() or "ibot" in message.content.lower() or "ilearner" in message.content.lower()) and message.author.id != 555845842662064128 and not message.author.bot:
        await handleMessage(message)

    if message.mentions:
        for member in message.mentions:
            if member.id == 379624030317182976:
                item = random.choice(quotes)
                await message.channel.send(item)
    await client.process_commands(message)


async def handleMessage(message):
    if "?" in message.content.lower() or "why" in message.content.lower() or "how" in message.content.lower() or "can i" in message.content.lower():
        item = random.choice(answers)
        await message.channel.send(item)
    else:
        item = random.choice(quotes)
        await message.channel.send(item)
