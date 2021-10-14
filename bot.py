import discord
from discord.ext import commands
from PIL import Image
import random

intents = discord.Intents.default()
intents.members = True

activity = discord.Activity(type=discord.ActivityType.watching, name = 'for someone to welcome!')
command_prefix = ">"

client = commands.Bot(command_prefix = ">", activity = activity, intents = intents)

filename = "LongChamp.png"

@client.event
async def on_ready():
    print('MerryBot is ready!')


@client.event
async def on_member_join(member):
    guild = client.get_guild(151883696964632577)
    channel = guild.get_channel(151883696964632577)
    await channel.send('Welcome!')

@client.event
async def on_message(message):
    if message.content == 'hi':
        await message.channel.send('hello!')

    elif message.content == 'Will an AI pass the Turing test by 2022?':
        await message.channel.send('uncertain')

    elif 'LongChamp' in message.content:
        await message.channel.send(file=discord.File('C:/Users/Kiffer/Desktop/MerryBot/LongChamp.png'))

    elif '?' in message.content:
        if random.random() <= .06:
            if random.random() <= .5:
                await message.channel.send('yes')
            else:
                await message.channel.send('no')

    elif  message.content == 'Milkcraate':
        await message.channel.send('hi I was just watching for a bit and wanted to say hi and I thought ur doing rly good')

    elif 'bingus' in message.content:
        switch = random.randint(0,4)
        if (switch == 0):
            await message.channel.send(file=discord.File('C:/Users/Kiffer/Desktop/MerryBot/bingus1.png'))

        elif (switch == 1):
            await message.channel.send(file=discord.File('C:/Users/Kiffer/Desktop/MerryBot/bingus2.JPG'))

        elif (switch == 2):
            await message.channel.send(file=discord.File('C:/Users/Kiffer/Desktop/MerryBot/bingus3.JPG'))

        elif (switch == 3):
            await message.channel.send(file=discord.File('C:/Users/Kiffer/Desktop/MerryBot/bingus4.png'))

        elif (switch == 4):
            await message.channel.send(file=discord.File('C:/Users/Kiffer/Desktop/MerryBot/bingus5.png'))



client.run('ODkwNjI1MzQ1NzA1ODk0MDAw.YUyhfQ.LwdvykPcRz4OuxDH-ReHLepAFqA')
