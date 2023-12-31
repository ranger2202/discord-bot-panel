from quart import Quart, render_template, request, jsonify
import discord
from discord.ext import commands
import asyncio
import threading

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
 
async def start_bot_async(bot_token):
    try:
        await bot.start(bot_token)
    except discord.LoginFailure:
        print("Invalid token")

def start_bot(bot_token):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot_async(bot_token))