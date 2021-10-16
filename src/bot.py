"""
Resources:
__________
https://discordpy.readthedocs.io/en/stable/
"""

import discord as dpy
import json
import random
import signal
import sys

from discord.ext import commands


intents = dpy.Intents.default()
intents.members = True

activity = dpy.Activity(type=dpy.ActivityType.watching,
                        name="for someone to welcome!")
prefix = '_'
interjections = [
    "hi",
    "hey",
    "hello",
    "howdy",
    "hi-ya",
    "hiya",
    "hallo",
    "greetings"
]
client = commands.Bot(command_prefix=prefix, activity=activity, intents=intents)

def signal_handle(sig, frame):
    client.logout()
    sys.exit(0)


@client.event
async def on_ready():
    if (not hasattr(client, "appinfo")):
        client.appinfo = await client.application_info()

    print(f"Application ID: {client.appinfo.id}")
    print("MerryBot is ready!")


@client.event
async def on_member_join(member):
    try:
        guild = client.get_guild(151883696964632577)
        channel = guild.get_channel(151883696964632577)
        await channel.send("Welcome!")
    except Forbidden:
        return
    except Exception as err:
        raise err


def _valid_message(msg):
    # Not in Social Category
    if (msg.channel.category_id != 885930648097927188):
        return False
    # bot_test channel and not test_bot id
    if (msg.channel.id == 898312842938318899 and
            client.appinfo.id != 439484187100184577):
        return False
    return True


def _bot_msg(msg):
    if (msg.author.bot):
        return True
    return False


@client.event
async def on_message(msg):
    if _bot_msg(msg): return
    try:
        await client.process_commands(msg)
    except commands.errors.CommandNotFound as err:
        cmd = msg.content.split()[0][1:]
        await msg.reply(f"{cmd} is not a valid command. @ cataSucc#0001 if you would like it added.")
        raise err

    if not _valid_message(msg): return

    msg.content = msg.content.lower()
    match msg.content:
        case "hi":
            try:
                await msg.channel.send(
                    interjections[random.randint(0, len(interjections)-1)])
            except Forbidden:
                pass
            except Exception as err:
                raise err

        case "will an ai pass the turing test by 2022?":
            await msg.channel.send("uncertain")

        case "longchamp":
            await msg.channel.send(file=dpy.File("./images/LongChamp.png"))

        case "milkcraate":
            await msg.channel.send("hi I was just watching for a bit and wanted\
 to say hi and I thought ur doing rly good")

    if "bingus" in msg.content:
        switch = random.randint(0, 4)
        match switch:
            case 0:
                await msg.channel.send(file=dpy.File("./images/bingus1.png"))

            case 1:
                await msg.channel.send(file=dpy.File("./images/bingus2.JPG"))

            case 2:
                await msg.channel.send(file=dpy.File("./images/bingus3.JPG"))

            case 3:
                await msg.channel.send(file=dpy.File("./images/bingus4.png"))

            case 4:
                await msg.channel.send(file=dpy.File("./images/bingus5.png"))

    elif ("?" in msg.content):
        if (random.random() < .06):
            if (random.random() <= .5):
                await msg.channel.send("yes")
            else:
                await msg.channel.send("no")


@client.command()
async def ping(ctx):
    if not _valid_message(ctx): return
    await ctx.channel.send("pong")


try:
    with open("login") as f:
        login = json.load(f)
except Exception as err:
    raise err
else:
    client.run(login["token"])
finally:
    signal.signal(signal.SIGINT, signal_handle)
