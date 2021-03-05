from dotenv import load_dotenv
import os

# lists
emoji_list = []
roster_list = []
muted_list = []

from main.main import client
from commands.tournament import cleanerkey, tourney, tourney_role, sendkeys
from commands.admin import tourneys, admin
from commands.emoji import addemoji, delemoji
from commands.roster import roster, droster, rosters
from commands.misc import mute, unmute, help
from commands.mc import server
from event import on_ready, on_guild_join, on_guild_remove, on_member_update, on_message


load_dotenv()
client.run(os.getenv("BOT_TOKEN"))
