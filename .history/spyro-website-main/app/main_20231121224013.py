# main.py
from quart import Quart, send_file, redirect, url_for, render_template
from discord.ext.ipc import Client
from quart_discord import DiscordOAuth2Session, requires_authorization
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Quart(__name__)
app.config["SECRET_KEY"] = "2424242424"
app.config["DISCORD_CLIENT_ID"] = 1153036881995501639
app.config["DISCORD_CLIENT_SECRET"] = "WSl31w9--ikAhFhZ2KC1AdHeX8xdN_Q9"
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:8000/callback"

ipc = Client(host="bot ip.", secret_key="Ph29G1ghT", multicast_port=5001)
discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
    # Pass user authentication status and user's avatar URL to the template
    return await render_template("index.html", user_authenticated=current_user.is_authenticated, user_avatar=current_user.avatar_url)

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
    except Exception as e:
        print(f"Callback error: {e}")
        return redirect(url_for("dashboard"))
    guild_count = await ipc.request("get_guild_count")
    return f"The bot is in: {guild_count} servers"

if __name__ == "__main__":
    app.run(debug=True, port=8000)