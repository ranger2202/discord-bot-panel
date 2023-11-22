# main.py

from quart import Quart, send_file, redirect, url_for, render_template
from discord.ext.ipc import Client
from quart import session
from quart_discord import DiscordOAuth2Session

app = Quart(__name__)
app.config["SECRET_KEY"] = "2424242424"
app.config["DISCORD_CLIENT_ID"] = 1153036881995501639
app.config["DISCORD_CLIENT_SECRET"] = "WSl31w9--ikAhFhZ2KC1AdHeX8xdN_Q9"
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:8000/callback"

ipc = Client(host="localhost", secret_key="Ph29G1ghT", multicast_port=5001)
discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
    # Check if the user is authenticated
    user_authenticated = "discord_token" in session

    # If authenticated, get the user's avatar URL
    user_avatar = ""
    if user_authenticated:
        discord = DiscordOAuth2Session(app)
        user = await discord.fetch_user()
        user_avatar = user.avatar_url

    # Pass user authentication status and user's avatar URL to the template
    return await render_template("index.html", user_authenticated=user_authenticated, user_avatar=user_avatar)

@app.route("/dashboard")
@requires_authorization
async def dashboard():
    user = await discord.fetch_user()
    return user.name

@app.route("/login")
async def login():
    return await discord.create_session()

@app.route("/callback")
async def callback():
    try:
        await discord.callback()
        # Assuming you want to check the guild count after authentication
        guild_count = await ipc.request("get_guild_count")
        return f"The bot is in: {guild_count} servers"
    except Exception as e:
        print(f"Callback error: {e}")
        return redirect(url_for("dashboard"))

if __name__ == "__main__":
    try:
        # Attempt to connect to the IPC server
        ipc.connect()
    except Exception as e:
        print(f"IPC connection error: {e}")
    
    app.run(debug=True, port=8000)
