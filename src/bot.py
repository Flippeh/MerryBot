""" MerryBot
Resources:
__________
https://docs.pycord.dev/en/master/index.html
"""

from pathlib import Path

import json
import random
import signal
import sys
import types
import discord as dpy

from discord.ext import commands
# pylint: disable=W0401
# pylint: disable=E0401
# pylint: disable=W0611
from cmds import mock, new_bingus, perms, ping, power
from lib import depricated, download, msgcheck

import logger as lgr

INTENTS = dpy.Intents.default()
# pylint: disable=E0237
# NOTE: This is not an error. This is how py-cord describes to modify the bots intents.
# NOTE: This is to see member join/leave events
INTENTS.members = True

ACTIVITY = dpy.Activity(type=dpy.ActivityType.watching,
                        name="for someone to welcome!")
# TODO: Have these variables stored in a yaml file and read on init
PREFIX = '_'
INTERJECTIONS = [
    "hi",
    "hey",
    "hello",
    "howdy",
    "hiya",
    "greetings"
]
EMOJIES = ["🔁", "⛔"]

client = commands.Bot(command_prefix=PREFIX, activity=ACTIVITY, intents=INTENTS)
log = lgr.get_logger()


async def bot_exit(channel=None):
    if channel:
        await channel.send('Bye!')
    await client.close()
    sys.exit(0)


# pylint: disable=W0613
def signal_handle(sig, frame):
    bot_exit()
# pylint: enable=W0613

@client.event
async def on_connect():
    """ Makes sure that client.appinfo is populated """
    if not hasattr(client, "appinfo"):
        client.appinfo = await client.application_info()


@client.event
async def on_ready():
    """ Initializes the bot """
    import_list = []
    log.debug("began initialization")
    for _, val in globals().items():
        if isinstance(val, types.ModuleType):
            if val.__name__[:4] == "cmds":
                log.debug(f"Found command {val.__name__} ...")
                import_list.append((val.__name__[5:], val))

    errored = []
    for i in import_list:
        try:
            cmd = commands.Command(name=i[0], func=i[1].cmd)
        except AttributeError as err:
            log.error(err)
            errored.append(i)
        except TypeError as err:
            log.error(err)
            errored.append(i)
        try:
            client.add_command(cmd)
            print(f"Success adding {i[0]} ...")
        except Exception:
            print(f"Error adding {i[0]} as a command...")


    for i in errored:
        log.info(f"Command {i[0]} errored during initialization...")

    print(f"Application ID: {client.appinfo.id}")
    print("MerryBot is ready!")
    print(f"Commands: {client.all_commands}")


# pylint: disable=W0613
@client.event
async def on_member_join(member):
    """ When a new user joins the guild """
    if msgcheck.test_bot(client):
        return
    try:
        guild = client.get_guild(151883696964632577)
        channel = guild.get_channel(151883696964632577)
        await channel.send("Welcome!")
    except dpy.Forbidden:
        return
    except Exception as err:
        raise err


@client.event
async def on_command_error(ctx, error):
    """ Handles errors from running commands """
    if isinstance(error, commands.errors.CommandNotFound):
        cmd = ctx.message.content.split()[0][1:]
        await ctx.send(
            f":scream: `{cmd}` is not a valid command. If you would like it " \
            "added create an issue on my repo and give it the label " \
            "enhancement` :arrow_right: " \
            "https://github.com/Flippeh/MerryBot/issues")
    elif isinstance(error.__cause__, NotImplementedError):
        cmd = ctx.message.content.split()[0][1:]
        await ctx.send(
            f":scream: `{cmd}` is not written yet. If you would like it added" \
            " create an issue on my repo and give it the label `enhancement` " \
            ":arrow_right: https://github.com/Flippeh/MerryBot/issues")
    else:
        print(type(error), error)
        raise error


def get_random_bingus() -> Path:
    images = Path('./images/bingus/').glob('*')
    files = [x for x in images if x.is_file()]
    chosen = files[random.randint(0, len(files) - 1)]
    return chosen


@client.event
async def on_message(msg):
    """ Event action for new messages """
    # If message was sent by a bot then exit
    if msgcheck.bot_msg(msg):
        return

    # If the message is in the test channel and not the test bot, exit
    if msgcheck.test_channel(msg.channel) and not msgcheck.test_bot(client):
        return

    # Process command functions
    await client.process_commands(msg)

    # If the message is not in a valid channel exit.
    # NOTE: This would be depricated in the case where this bot replaces Auburn Esports#3661
    if not msgcheck.valid_channel(msg.channel):
        return

    msg.content = msg.content.lower()
    match msg.content:
        case "hi":
            await msg.channel.send(INTERJECTIONS[random.randint(0, len(INTERJECTIONS)-1)])
            return

        case "will an ai pass the turing test by 2022?":
            await msg.channel.send("uncertain")
            return

        case "milkcraate":
            await msg.channel.send("hi I was just watching for a bit and wanted\
 to say hi and I thought ur doing rly good")
            return

    if "longchamp" in msg.content:
        await msg.channel.send(file=dpy.File("./images/LongChamp.png"))
        return

    if "bingus" in msg.content:
        if "bingus --list-all" in msg.content:
            images = Path('./images/bingus/').glob('*')
            files = [x for x in images if x.is_file()]
            for picture in files:
                await msg.channel.send(f"Name: {picture}", file=dpy.File(picture))
        else:
            bingus_path = get_random_bingus()
            await msg.channel.send(file=dpy.File(bingus_path))
        return

    if "?" in msg.content:
        if random.random() < .06:
            if random.random() <= .5:
                await msg.channel.send("yes")
            else:
                await msg.channel.send("no")


@client.command()
@commands.has_permissions(administrator=True)
async def update(ctx):
    raise NotImplementedError


def main():
    """ Init method """

    try:
        with open("login", encoding="UTF-8") as file:
            login = json.load(file)
    except Exception as err:
        log.error(err)
        raise err
    else:
        client.run(login["token"])
    finally:
        signal.signal(signal.SIGINT, signal_handle)


if __name__ == '__main__':
    main()
