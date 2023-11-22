# main.py
from quart import Quart, send_file, redirect, url_for, render_template, session
from discord.ext.ipc import Client
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import os
import quart_discord

app = Quart(__name__)
app.config["SECRET_KEY"] = "2424242424"
app.config["DISCORD_CLIENT_ID"] = 1153036881995501639
app.config["DISCORD_CLIENT_SECRET"] = "WSl31w9--ikAhFhZ2KC1AdHeX8xdN_Q9"
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:8000/callback"

ipc = Client(host="bot ip.", secret_key="Ph29G1ghT", multicast_port=5001)
discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
    user = session.get("discord_user")
    return await render_template("index.html", user=user)

@app.route("/dashboard")
@requires_authorization
async def dashboard():
    user = session.get("discord_user")
    return await render_template("dashboard.html", user=user)

@app.route("/login")
async def login():
    return await discord.create_session()

@app.route("/callback")
async def callback():
    try:
        await discord.callback()
        user = await discord.fetch_user()
        session["discord_user"] = {
            "id": user.id,
            "username": user.name,
            "discriminator": user.discriminator,
            "avatar_url": str(user.avatar.url) if user.avatar else None,
        }
    except Exception as e:
        print(f"Callback error: {e}")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
