from pathlib import Path

import asyncio
import functools
import warnings
import urllib

import bot

async def download(url, dest: Path):
    """ Downloads from the url and saves to a destination """
    print(url)
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
    headers = {"User-Agent": user_agent}
    req = urllib.request.Request(url, {}, headers)
    with urllib.request.urlopen(req) as webfile:
        with open(dest.resolve(), 'wb') as localfile:
            localfile.write(webfile.read())
