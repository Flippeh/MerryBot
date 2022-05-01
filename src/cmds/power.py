""" power
"""
# NOTE: This command does not work at the moment.

import asyncio
import lib

from discord.ext import commands

import bot

@commands.has_permissions(administrator=True)
async def cmd(ctx):
    """ command to power off and restart the bot """
    msg = await ctx.channel.send("Select what you would like to do...")
    for emoji in bot.EMOJIES:
        await msg.add_reaction(emoji)

    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) in bot.EMOJIES

    try:
        # NOTE: This does not check if the right user has reacted.
        # pylint: disable=W0612
        reaction, user = await bot.client.wait_for('reaction_add', timeout=10.0, check=check)
    except asyncio.TimeoutError:
        await ctx.channel.send('👎')
    else:
        if str(reaction.emoji) == "🔁":
            await ctx.channel.send("rebooting not supported yet.")

        if str(reaction.emoji) == "⛔":
            await ctx.channel.send("Shutting down.")
            await bot_exit(ctx.channel)
