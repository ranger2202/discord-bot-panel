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
app.config["DISCORD_CLIENT_ID"] = 1131320139141365871
app.config["DISCORD_CLIENT_SECRET"] = "SlT2BHrnVdL6O-sVPOWU5iuIB6zAuyep"
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:8000/callback/discord"
app.config["ROBLOX_CLIENT_ID"] = "6841966900709651411"
app.config["ROBLOX_CLIENT_SECRET"] = "RBX-3TM2HZggakGl-47YSbs2tspB_0PMi5Axy7F26_T60a2Zs_ZXpSXGaas08Egra3mo"
app.config["ROBLOX_REDIRECT_URI"] = "http://localhost:8000/callback/roblox"

ipc = Client()
discord = DiscordOAuth2Session(app)

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
    discord.revoke()
    return redirect(url_for("home"))


To achieve the functionality you described, you'll need to modify the dashboard route in your backend code to retrieve the user's servers and check if the user has administrator permissions in any of those servers. Additionally, you should pass the relevant server information (name and logo) to the template for rendering.

Here's an example modification to your backend code:

python
Copy code
# Update the dashboard route
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

        # Get the user's guilds (servers)
        guilds = await discord.fetch_guilds()
        
        # Check if the user has administrator permissions in any server
        admin_servers = [guild for guild in guilds if discord.is_administrator(guild)]
        
        if admin_servers:
            # Assuming you want to display information about the first admin server
            admin_server = admin_servers[0]
            
            # Get the server name and logo
            server_name = admin_server.name
            server_logo = f"https://cdn.discordapp.com/icons/{admin_server.id}/{admin_server.icon}.png"
            
            # Pass the server information to the template
            return await render_template("server-select.html", user=session["discord_user"], server_name=server_name, server_logo=server_logo)
        else:
            return await render_template("server-select.html", user=session["discord_user"], server_name=None, server_logo=None)
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