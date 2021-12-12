""" MerryBot
Resources:
__________
https://discordpy.readthedocs.io/en/stable/
"""

import asyncio
import json
import random
import signal
import sys
import urllib.request

from pathlib import Path
from discord.ext import commands

import discord as dpy


INTENTS = dpy.Intents.default()
# pylint: disable=E0237
# NOTE: This is not an error. This is how discord.py describes to modify the bots intents.
INTENTS.members = True

ACTIVITY = dpy.Activity(type=dpy.ActivityType.watching,
                        name="for someone to welcome!")
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
async def on_ready():
    """ Initializes the bot """
    if not hasattr(client, "appinfo"):
        client.appinfo = await client.application_info()

    print(f"Application ID: {client.appinfo.id}")
    print("MerryBot is ready!")


def _test_bot():
    # Return false if test bot id
    return client.appinfo.id == 439484187100184577


def _test_channel(channel):
    # bot_test channel
    return channel.id == 898312842938318899


def _valid_channel(channel):
    # Return 'valid' if in social category
    return channel.category_id == 885930648097927188


def _valid_message(msg):
    return _valid_channel(msg.channel) and _test_bot()

# pylint: disable=W0613
@client.event
async def on_member_join(member):
    """ When a new user joins the guild """
    if _test_bot():
        return
    try:
        guild = client.get_guild(151883696964632577)
        channel = guild.get_channel(151883696964632577)
        await channel.send("Welcome!")
    except dpy.Forbidden:
        return
    except Exception as err:
        raise err


def _bot_msg(msg):
    return msg.author.bot


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
    if _bot_msg(msg):
        return


    # If the message is in the test channel and not the test bot, exit
    if _test_channel(msg.channel) and not _test_bot():
        return

    # Process command functions
    await client.process_commands(msg)

    if not _valid_channel(msg.channel):
        return

    msg.content = msg.content.lower()
    match msg.content:
        case "hi":
            await msg.channel.send(INTERJECTIONS[random.randint(0, len(INTERJECTIONS)-1)])

        case "will an ai pass the turing test by 2022?":
            await msg.channel.send("uncertain")

        case "milkcraate":
            await msg.channel.send("hi I was just watching for a bit and wanted\
 to say hi and I thought ur doing rly good")

    if "longchamp" in msg.content:
        await msg.channel.send(file=dpy.File("./images/LongChamp.png"))

    if "bingus" in msg.content:
        if "bingus --list-all" in msg.content:
            images = Path('./images/bingus/').glob('*')
            files = [x for x in images if x.is_file()]
            for picture in files:
                await msg.channel.send(f"Name: {picture}", file=dpy.File(picture))
        else:
            bingus_path = get_random_bingus()
            await msg.channel.send(file=dpy.File(bingus_path))

    if "?" in msg.content:
        if random.random() < .06:
            if random.random() <= .5:
                await msg.channel.send("yes")
            else:
                await msg.channel.send("no")


@client.command()
async def ping(ctx):
    if not _valid_message(ctx):
        return
    await ctx.channel.send("pong")


@client.command()
async def mock(ctx, *args):
    if not _valid_message(ctx):
        return
    await ctx.channel.send(" ".join(args))


@client.command()
async def perms(ctx):
    if not _valid_message(ctx):
        return
    await ctx.channel.send(f"You have {ctx.author.permissions_in(ctx.channel)} permissions")


def _check(reaction, user):
    print(user, reaction.message.author)
    return user == reaction.message.author and str(reaction.emoji) in EMOJIES


@client.command()
@commands.has_permissions(administrator=True)
async def power(ctx):
    """ command to power off and restart the bot """
    if not _valid_message(ctx):
        return
    msg = await ctx.channel.send("Select what you would like to do...")
    for emoji in EMOJIES:
        await msg.add_reaction(emoji)

    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) in EMOJIES

    try:
        # NOTE: This does not check if the right user has reacted.
        # pylint: disable=W0612
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.channel.send('👎')
    else:
        if str(reaction.emoji) == "🔁":
            await ctx.channel.send("rebooting not supported yet.")

        if str(reaction.emoji) == "⛔":
            await ctx.channel.send("Shutting down.")
            await bot_exit(ctx.channel)


async def download(url, dest: Path):
    """ Downloads from the url and saves to a destination """
    print(url)
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
    headers = {"User-Agent": user_agent}
    req = urllib.request.Request(url, {}, headers)
    with urllib.request.urlopen(req) as webfile:
        with open(dest.resolve(), 'wb') as localfile:
            localfile.write(webfile.read())


@client.command()
@commands.has_permissions(administrator=True)
async def new_bingus(ctx):
    """ Creates a new bingus image """
    if not _valid_message(ctx):
        return
    if len(ctx.message.attachments) > 0:
        image = ctx.message.attachments[0].url
        await ctx.channel.send(image)
        images = Path('./images/bingus/').glob('*')
        num = len([x for x in images if x.is_file()])
        file = Path(f"./images/bingus/bingus{num+1}.{image[-3:]}")
        await download(image, file)
    else:
        await ctx.channel.send("No attachments found in your message")


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
        raise err
    else:
        client.run(login["token"])
    finally:
        signal.signal(signal.SIGINT, signal_handle)

if __name__ == '__main__':
    main()
