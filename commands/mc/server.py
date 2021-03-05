import discord
from discord.ext import commands

from iBot import client
from mcstatus import MinecraftServer
from time import localtime, strftime

from utils.functions import sendError


@client.command()
async def server(ctx, ip: str, port=None):
    if port is None:
        port = "25565"

    server = MinecraftServer.lookup(f"{ip}:{port}")
    status = server.status()
    query = server.query()
    member = ctx.message.author
    deletmsgdebug = ''
    msgtime = strftime("%d/%m/%Y [%I:%M:%S %p] (%Z)", localtime())
    usermsg = "{0}".format(client.name).replace("'", "")
    motd = query.motd.replace("§b§", "").replace("§f", "").replace("§2", "").replace("§a", "").replace("§4", "")
    em = discord.Embed(title=motd, description=deletmsgdebug, colour=0x2ecc71)

    latency = server.ping()

    players = "Players: {0}/{1} | Ping: {2}ms | Version: {3}".format(status.players.online, status.players.max,
                                                                     latency, query.software.version)
    em.add_field(name="Status", value=players)

    playerlist = "{0}".format(", ".join(query.players.names))
    em.add_field(name="Playerlist", value=playerlist)

    em.set_author(name=usermsg, icon_url=client.avatar_url)
    em.set_footer(text=msgtime, icon_url=member.avatar_url)
    await ctx.message.channel.send(embed=em)


@server.error
async def server_error(ctx, error):
    if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        await sendError("***Usage:*** iserver ip port(optional)\n\nQuery a minecraft server by `ip` and `port`", "", ctx)
    else:
        await sendError("Failed to query server!\n\nMake sure the server has query enabled!\n", "", ctx)
