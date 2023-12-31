from quart import Quart, render_template, request, jsonify
import discord
from discord.ext import commands
import asyncio

app = Quart(__name__)

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@app.route('/')
async def home():
    return await render_template('landing.html')

async def start_bot_task(bot_token):
    try:
        await bot.start(bot_token)
    except discord.LoginFailure:
        print("Invalid token")

# Define the route for starting the bot
@app.route("/start_bot", methods=['POST'])
async def start_bot():
    try:
        async with app.app_context():
            data = await request.json
            bot_token = data.get("bot_token") 
            if bot_token:
                asyncio.create_task(start_bot_task(bot_token))
                return jsonify({"message": f"success"})
            else:
                return jsonify({"error": "No bot_token provided in the request"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)