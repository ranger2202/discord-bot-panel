from quart import Quart, render_template, request, jsonify
import discord
from discord.ext import commands
import asyncio
import threading
from 



def start_bot(bot_token):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot_async(bot_token))