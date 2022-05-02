from pathlib import Path

import asyncio
import functools
import warnings
import urllib

import bot

def bot_msg(msg):
    # Return true if msg author is a bot
    return msg.author.bot


def test_bot(client):
    # Return false if test bot id
    return client.appinfo.id == 439484187100184577


def test_channel(channel):
    # bot_test channel
    return channel.id == 898312842938318899


def valid_channel(channel):
    # Return true if in social category
    return channel.category_id == 885930648097927188
