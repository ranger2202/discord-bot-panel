from quart import Quart, render_template, request, jsonify
import discord
from discord.ext import commands
import asyncio
import threading

app = Quart(__name__)
loop = asyncio.get_event_loop()

custom_commands = {}


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!') and message.content[1:] in custom_commands:
        response = custom_commands[message.content[1:]]
        await message.channel.send(response)

    await bot.process_commands(message)

async def start_bot_async(bot_token):
    try:
        await bot.start(bot_token)
    except discord.LoginFailure:
        print("Invalid token")

def start_bot(bot_token):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot_async(bot_token))

@app.route('/')
async def home():
    return await render_template('landing.html')


@app.route("/stop_bot", methods=['POST'])
async def stop_bot():
    try:
        if bot.is_ready():
            await bot.close()
            return jsonify({'status': 'success', 'message': 'Bot stopped successfully'})
        else:
            return jsonify({'status': 'not_running', 'message': 'The bot is not currently running.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route("/check_bot_status", methods=['GET'])
async def check_bot_status():
    try:
        return jsonify({'status': 'running' if bot.is_ready() else 'not_running'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route("/addcommands", methods=['POST'])
async def add_commands_route():
    try:
        async with app.app_context():
            data = await request.json
            commands_list = data.get("commands_list")

            if commands_list and isinstance(commands_list, list):
                for cmd in commands_list:
                    command_name = cmd.get("command_name")
                    response = cmd.get("response")
                    if command_name and response:
                        custom_commands[command_name.lower()] = response
                return jsonify({"message": "Custom commands added successfully!"})
            else:
                return jsonify({"error": "Invalid data provided"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})


@app.route("/start_bot", methods=['POST'])
async def start_bot_route():
    try:
        async with app.app_context():
            data = await request.json
            bot_token = data.get("bot_token")
            if bot_token:
                loop = asyncio.get_event_loop()
                loop.create_task(start_bot_async(bot_token))
                return jsonify({"message": f"Successfully turned on bot {bot.user.name} (ID: {bot.user.id})"})
            else:
                return jsonify({"error": "No bot_token provided in the request"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})

if __name__ == '__main__':
    loop.create_task(start_bot_async())
    app.run(debug=True, port=5000)
