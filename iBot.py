from dotenv import load_dotenv
import dbl
import os

# lists
emoji_list = []
roster_list = []
muted_list = []

from main.main import client, dbl_client
from commands.tournament import cleanerkey, tourney, tourney_role, sendkeys
from commands.admin import tourneys, admin
from commands.emoji import addemoji, delemoji
from commands.roster import roster, droster, rosters
from commands.misc import help
from commands.mute import mute, unmute
from commands.mc import server
from event import on_ready, on_guild_join, on_guild_remove, on_member_update, on_message
from topgg.event import on_dbl_vote


load_dotenv()
client.run(os.getenv("BOT_TOKEN"))
