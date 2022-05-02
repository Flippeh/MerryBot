from pathlib import Path

import asyncio
import functools
import warnings
import urllib

import bot

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func


def _bot_msg(msg):
    # Return true if msg author is a bot
    return msg.author.bot


def _test_bot(client):
    # Return false if test bot id
    return client.appinfo.id == 439484187100184577


def _test_channel(channel):
    # bot_test channel
    return channel.id == 898312842938318899


def _valid_channel(channel):
    # Return true if in social category
    return channel.category_id == 885930648097927188


async def download(url, dest: Path):
    """ Downloads from the url and saves to a destination """
    print(url)
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
    headers = {"User-Agent": user_agent}
    req = urllib.request.Request(url, {}, headers)
    with urllib.request.urlopen(req) as webfile:
        with open(dest.resolve(), 'wb') as localfile:
            localfile.write(webfile.read())
