""" new_bingus
"""
from pathlib import Path

import asyncio
import lib

from discord.ext import commands

@commands.has_permissions(administrator=True)
async def cmd(ctx):
    """ Creates a new bingus image """
    if len(ctx.message.attachments) > 0:
        image = ctx.message.attachments[0].url
        await ctx.channel.send(image)
        images = Path('./images/bingus/').glob('*')
        num = len([x for x in images if x.is_file()])
        file = Path(f"./images/bingus/bingus{num+1}.{image[-3:]}")
        await lib.download(image, file)
    else:
        await ctx.channel.send("No attachments found in your message")
