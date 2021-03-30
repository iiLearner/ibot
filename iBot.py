import logging
import os
from dotenv import load_dotenv
from logs.IBotLogging import IBotLogging

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.INFO)
discord_logger.addHandler(IBotLogging())

# lists
emoji_list = []
roster_list = []
muted_list = []

from main.main import client
from commands.tournament import cleanerkey, tourney, tourney_role, sendkeys
from commands.admin import tourneys, admin
from commands.emoji import addemoji, delemoji
from commands.roster import roster, droster, rosters
from commands.misc import help
from commands.mute import mute, unmute
from commands.mc import server
from event import on_ready, on_guild_join, on_member_update, on_message


load_dotenv()
client.run(os.getenv("BOT_TOKEN"))
