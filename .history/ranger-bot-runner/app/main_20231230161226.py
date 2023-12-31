from quart import Quart, render_template, request, jsonify
import discord
from discord.ext import commands
import asyncio

app = Quart(__name__)

# Dictionary to store custom commands
custom_commands = {}

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Define the on_ready event
@bot.event
async def on_ready():
    print(f"Bot is ready: {bot.user.name} (ID: {bot.user.id})")

# Define a custom command to add new commands
@bot.command(name='addcommand')
async def add_command(ctx, command_name, *, response):
    """
    Add a new custom command.
    Example: !addcommand greet Hey, how are you?
    """
    custom_commands[command_name.lower()] = response
    await ctx.send(f"Custom command '{command_name}' added!")

# Define a command to use custom commands
@bot.command(name='usecommand')
async def use_command(ctx, command_name):
    """
    Use a custom command.
    Example: !usecommand greet
    """
    response = custom_commands.get(command_name.lower(), "Command not found.")
    await ctx.send(response)

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
