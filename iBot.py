import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# lists
emoji_list = []
roster_list = []
muted_list = []


intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = commands.Bot(command_prefix='?', intents=intents, activity=discord.Streaming(name="iBotting", url="https://www.twitch.tv/kaeratrbl"))
from commands.tournament import cleanerkey, tourney, tourney_role, sendkeys
from commands.admin import tourneys
from events import on_ready, on_guild_join, on_guild_remove, on_member_update, on_message, on_raw_reaction_add
from commands import adduser, removeuser, basic_commands, roster, mute


load_dotenv()
client.run(os.getenv("BOT_TOKEN"))
