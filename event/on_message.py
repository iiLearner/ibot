import random
import discord
import time
from emoji.emoji import delete_emoji
from iBot import client, emoji_list, muted_list
from mute.mute import delMute, isMuted
from reaction.reaction import getReactionTime, setReactionTime
from strings.quotes import quotes, answers


@client.event
async def on_message(message):
    # we dont handle anything from ibot itself
    if message.author.id == client.user.id:
        return

    if not isinstance(message.channel, discord.abc.PrivateChannel):
        await handleMute(message)

        if not await isMuted(message.author.id, message.channel.guild.id):
            await handleReaction(message)
            if 'cj' in message.content.lower() or "ibot" in message.content.lower() or "ilearner" in message.content.lower():
                if not message.author.bot:
                    await handleMessage(message)
                elif message.author.bot and message.author.id == 787744892813312082 and "ilearner" not in message.content.lower():
                    await handleMessage(message)

            if message.mentions:
                await handleMention(message)

    if isinstance(message.channel, discord.abc.PrivateChannel):
        await handleDm(message)

    await client.process_commands(message)


async def handleMute(message):
    for x in muted_list:
        if x.user == message.author.id and x.server == message.channel.guild.id:
            try:
                await message.delete()
                return True
            except Exception as e:
                await delMute(message.author.id, message.channel.guild.id)


async def handleReaction(message):

    for x in emoji_list:
        if message.channel.guild.id == x.server and message.author.id == x.user:
            cur_time = int(time.time())
            last_reaction_time = await getReactionTime(message.author.id)
            if (cur_time - last_reaction_time) > 2 and not await isMuted(message.author.id, message.channel.guild.id):
                try:
                    emoji = client.get_emoji(x.emoji)
                    await message.add_reaction(emoji)
                    setReactionTime(message.author.id, cur_time)
                except discord.errors.HTTPException:
                    await delete_emoji(emoji.id, x.user, message.channel.guild.id)


async def handleMention(message):
    for member in message.mentions:
        if member.id == 379624030317182976:
            item = random.choice(quotes)
            await message.channel.send(item)


async def handleDm(message):
    item = random.choice(quotes)
    await message.channel.send(item)


async def handleMessage(message):
    if "?" in message.content.lower() or "why" in message.content.lower() or "how" in message.content.lower() or "can i" in message.content.lower():
        item = random.choice(answers)
        await message.channel.send(item)
    else:
        item = random.choice(quotes)
        await message.channel.send(item)


@client.check_once
async def check_commands(ctx):
    return not await isMuted(ctx.message.author.id, ctx.message.channel.guild.id)
