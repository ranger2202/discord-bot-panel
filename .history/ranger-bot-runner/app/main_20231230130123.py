from quart import Quart, render_template, request, jsonify
import discord
from discord.ext import commands
import asyncio

app = Quart(__name__)

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot_info = None

@bot.event
async def on_ready():
    global bot_info
    bot_info = {
        "name": bot.user.name,
        "id": bot.user.id
    }
    

@app.route('/')
async def home():
    return await render_template('landing.html')

async def start_bot_task(bot_token):
    try:
        await bot.start(bot_token)
    except discord.LoginFailure:
        print("Invalid token")



@app.route("/start_bot", methods=['POST'])
async def start_bot():
    try:
        async with app.app_context():
            data = await request.json
            bot_token = data.get("bot_token") 
            if bot_token:
                asyncio.create_task(start_bot_task(bot_token))
                return jsonify({"message": f"Successfully turned on bot {bot_info['name']} (ID: {bot_info['id']})"})
            else:
                return jsonify({"error": "No bot_token provided in the request"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})


# Add this route to your Flask app
@app.route("/addcommand", methods=['POST'])
async def add_command():
    try:
        async with app.app_context():
            data = await request.json
            command_name = data.get("command_name")
            response = data.get("response")

            if command_name and response:
                # Add the custom command to the dictionary
                custom_commands[ command_name.lower()] = response
                return jsonify({"message": f"Custom command '{command_name}' added!"})
            else:
                return jsonify({"error": "Invalid data provided"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
