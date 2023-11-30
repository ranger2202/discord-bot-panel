import sys
sys.dont_write_bytecode = True
from quart import Quart, send_file, redirect, url_for, render_template, session
from discord.ext.ipc import Client
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import os
import quart_discord
import requests
app = Quart(__name__)
app.config["SECRET_KEY"] = "2424242424"
app.config["DISCORD_CLIENT_ID"] = 1131320139141365871
app.config["DISCORD_CLIENT_SECRET"] = "SlT2BHrnVdL6O-sVPOWU5iuIB6zAuyep"
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:8000/callback/discord"

ipc = Client(host="bot ip.", secret_key="Ph29G1ghT", multicast_port=5001)
discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
    user = session.get("discord_user")
    return await render_template("landing.html", user=user)

@app.route("/robloxlink")
async def robloxlink():
    auth_payload = {
            'discord_id': str(interaction.user.id),
            'secret_key': SECRET_KEY
        }
    print(interaction.user.id)
    response = requests.post(f'{base_url}/auth', params=auth_payload)
    
    data = response.json()

    auth_url = data['authUrl']
    params = {
        'discord_id': str(interaction.user.id),
    }
    response = requests.get(f'{base_url}/getRobloxID', params=params)
    data = response.json()
    if 'userRobloxID' in data:
        user_roblox_id = data['userRobloxID']
        user = await client.get_user(user_roblox_id)


@app.route("/logout")
async def logout():
    session.pop("discord_user", None)
    discord.revoke()
    return redirect(url_for("home"))

@app.route("/dashboard")
@requires_authorization
async def dashboard():
    user = await discord.fetch_user()
    session["discord_user"] = {
        "id": user.id,
        "username": user.name,
        "discriminator": user.discriminator,
        "avatar_url": str(user.avatar_url) if user.avatar_url else None
    }
    return await render_template("landing.html", user=session["discord_user"])

@app.route("/login")
async def login():
    return await discord.create_session()

@app.route("/callback/discord")
async def callback():
    try:
        await discord.callback()
        user = await discord.fetch_user()
        session["discord_user"] = {
            "id": user.id,
            "username": user.name,
            "discriminator": user.discriminator,
            "avatar_url": str(user.avatar.url) if user.avatar else None
        }
    except Exception as e:
        print(f"Callback error: {e}")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True, port=8000)