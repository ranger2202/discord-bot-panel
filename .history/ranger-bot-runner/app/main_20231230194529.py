from quart import Quart, render_template, request, jsonify
import discord
from discord.ext import commands
import asyncio

app = Quart(__name__)

# Dictionary to store custom commands
custom_commands = {}

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Event to process messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    # Check if the message starts with the command prefix and is a custom command
    if message.content.startswith('!') and message.content[1:] in custom_commands:
        response = custom_commands[message.content[1:]]
        await message.channel.send(response)

    # Process other commands (if needed)
    await bot.process_commands(message)

# Add this route to your Quart app
@app.route('/')
async def home():
    return await render_template('landing.html')

# Add this route to your Quart app
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

# Add this route to your Quart app
@app.route("/start_bot", methods=['POST'])
async def start_bot():
    try:
        async with app.app_context():
            data = await request.json
            bot_token = data.get("bot_token") 
            if bot_token:
                asyncio.create_task(start_bot_task(bot_token))
                return jsonify({"message": f"Successfully turned on bot {bot.user.name} (ID: {bot.user.id})"})
            else:
                return jsonify({"error": "No bot_token provided in the request"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})

async def start_bot_task(bot_token):
    try:
        await bot.start(bot_token)
    except discord.LoginFailure:
        print("Invalid token")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
