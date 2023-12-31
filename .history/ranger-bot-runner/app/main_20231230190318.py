import threading
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
        return 

    if message.content.startswith('!') and message.content[1:] in custom_commands:
        response = custom_commands[message.content[1:]]
        await message.channel.send(response)

    # Process other commands (if needed)
    await bot.process_commands(message)

def run_bot():
    bot.run('YOUR_BOT_TOKEN')  # Replace 'YOUR_BOT_TOKEN' with your actual bot token

# Add this route to your Quart app
@app.route('/')
async def home():
    return await render_template('landing.html')

# Add this route to your Quart app
@app.route("/addcommand", methods=['POST'])
async def add_command_route():
    try:
        async with app.app_context():
            data = await request.json
            command_name = data.get("command_name")
            response = data.get("response")

            if command_name and response:
                # Add the custom command to the dictionary
                custom_commands[command_name.lower()] = response
                return jsonify({"message": f"Custom command '{command_name}' added!"})
            else:
                return jsonify({"error": "Invalid data provided"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})

# Add this route to your Quart app
@app.route("/start_bot", methods=['POST'])
async def start_bot():
    try:
        async with app.app_context():
            # Start the bot in a separate thread
            thread = threading.Thread(target=run_bot)
            thread.start()

            return jsonify({"message": f"Bot thread started successfully!"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
