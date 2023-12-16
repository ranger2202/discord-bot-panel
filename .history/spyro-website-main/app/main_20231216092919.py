import sys
sys.dont_write_bytecode = True
from quart import Quart, send_file, redirect, url_for, render_template, session, request
from discord.ext.ipc import Client
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import os
import json
import base64
import requests
import quart_discord
from roblox import Client

client = Client()

app = Quart(__name__)
app.config["SECRET_KEY"] = "2424242424"

ipc = Client()

async def setup_ipc():
    await ipc.connect("127.0.0.1", 5000)  # Use the same IP and port as your bot's IPC server

@app.route("/")
async def home():
    user = session.get("discord_user")
    return await render_template("landing.html", user=user)

@app.route('/redirect/roblox')
async def redirect_roblox():
    auth_url = f'https://apis.roblox.com/oauth/v1/authorize?client_id={app.config["ROBLOX_CLIENT_ID"]}&redirect_uri={app.config["ROBLOX_REDIRECT_URI"]}&scope=openid&response_type=code'
    return redirect(auth_url)
    

@app.route("/logout")
async def logout():
    session.pop("discord_user", None)
    await ipc.request("logout", {"user_id": str(session.get("discord_user", {}).get("id", ""))})
    return redirect(url_for("home"))

@app.route("/dashboard")
async def dashboard():
    try:
        user = await discord.fetch_user()
        session["discord_user"] = {
            "id": user.id,
            "username": user.name,
            "discriminator": user.discriminator,
            "avatar_url": str(user.avatar_url) if user.avatar_url else None
        }
        return await render_template("landing.html", user=session["discord_user"])
    except Unauthorized:
        return redirect(url_for("login"))

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

@app.route("/callback/roblox")
async def roblox_callback():
    code = request.args.get("code")
    
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": app.config["ROBLOX_CLIENT_ID"],
        "client_secret": app.config["ROBLOX_CLIENT_SECRET"],
        "redirect_uri": app.config["ROBLOX_REDIRECT_URI"]
    }
    user = await discord.fetch_user()
    session["discord_user"] = {
        "id": user.id,
        "username": user.name,
        "discriminator": user.discriminator,
        "avatar_url": str(user.avatar_url) if user.avatar_url else None
    }
    r = requests.post("https://apis.roblox.com/oauth/v1/token", data=data)
    r.raise_for_status()
    response = r.json()
    access_token = response['access_token']
    token_parts = access_token.split('.')
    claims_bytes = base64.b64decode(token_parts[1] + '===')
    claims_string = claims_bytes.decode('utf-8')
    claims = json.loads(claims_string)
    id = claims['sub']
    user = await client.get_user(id)
    print(user)
    user = await discord.fetch_user()
    session["discord_user"] = {
        "id": user.id,
        "username": user.name,
        "discriminator": user.discriminator,
        "avatar_url": str(user.avatar_url) if user.avatar_url else None
    }
    return await render_template("oauth.html", user=session["discord_user"])
   
@app.route("/oauth")
async def oauth_page():
    return await render_template("oauth.html", user=session.get("discord_user"))


if __name__ == "__main__":
    app.run(debug=True, port=8000)