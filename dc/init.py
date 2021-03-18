import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = commands.Bot(command_prefix='i', intents=intents, help_command=None, activity=discord.Streaming(name="iBotting", url=""))
