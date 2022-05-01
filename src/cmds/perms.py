import asyncio
import lib

from discord.ext import commands

import bot

async def cmd(ctx):
    await ctx.channel.send(f"You have {ctx.author.permissions_in(ctx.channel)} permissions")
