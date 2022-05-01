import asyncio
import lib

from discord.ext import commands


async def cmd(ctx, *args):
    await ctx.channel.send(" ".join(args))
