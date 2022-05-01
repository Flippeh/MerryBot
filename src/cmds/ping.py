import asyncio
import lib

from discord.ext import commands

async def cmd(ctx):
    await ctx.channel.send("pong")
