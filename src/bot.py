"""
Resources:
__________
https://discordpy.readthedocs.io/en/stable/
"""

import discord as dpy
import random
import json

from discord.ext import commands


intents = dpy.Intents.default()
intents.members = True

activity = dpy.Activity(type=dpy.ActivityType.watching,
                        name='for someone to welcome!')
command_prefix = ">"

client = commands.Bot(command_prefix=">", activity=activity, intents=intents)

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


@client.event
async def on_ready():
    if (not hasattr(client, 'appinfo')):
        client.appinfo = await client.application_info()

    print(f"Application ID: {client.appinfo.id}")
    print("MerryBot is ready!")


@client.event
async def on_member_join(member):
    guild = client.get_guild(151883696964632577)
    channel = guild.get_channel(151883696964632577)
    await channel.send('Welcome!')


@client.event
async def on_message(msg):
    if (msg.channel.category_id != 885930648097927188):
        return
    if (msg.channel.id == 898312842938318899 and
            client.appinfo.id != 439484187100184577):
        return

    msg.content = msg.content.lower()

    if ('?' in msg.content):
        if (random.random() <= .06):
            if (random.random() <= .5):
                await msg.channel.send('yes')
            else:
                await msg.channel.send('no')

    match msg.content:
        case "hi":
            await msg.channel.send(
                interjections[random.randint(0, len(interjections)-1)])

        case "will an ai pass the turing test by 2022?":
            await msg.channel.send('uncertain')

        case "longchamp":
            await msg.channel.send(file=dpy.File('./images/LongChamp.png'))

        case "milkcraate":
            await msg.channel.send('hi I was just watching for a bit and wanted\
 to say hi and I thought ur doing rly good')

    if "bingus" in msg.content:
        switch = random.randint(0, 4)
        match switch:
            case 0:
                await msg.channel.send(file=dpy.File('./images/bingus1.png'))

            case 1:
                await msg.channel.send(file=dpy.File('./images/bingus2.JPG'))

            case 2:
                await msg.channel.send(file=dpy.File('./images/bingus3.JPG'))

            case 3:
                await msg.channel.send(file=dpy.File('./images/bingus4.png'))

            case 4:
                await msg.channel.send(file=dpy.File('./images/bingus5.png'))


try:
    with open("login") as f:
        login = json.load(f)
except Exception as err:
    raise err
else:
    client.run(login["token"])
