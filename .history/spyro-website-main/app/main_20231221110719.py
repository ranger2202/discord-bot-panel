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
from discord.ext import ipc
from quart import Quart, jsonify, request
from dotenv import load_dotenv
client = Client()
load_dotenv()
SECRET_KEY = os.getenv('IPC_SECRET_KEY')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')


app = Quart(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["DISCORD_CLIENT_ID"] = CLIENT_ID
app.config["DISCORD_CLIENT_SECRET"] = CLIENT_SECRET
app.config["DISCORD_REDIRECT_URI"] = REDIRECT_URI

ipc_client = ipc.Client(host="localhost", secret_key=SECRET_KEY)
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

@app.route("/dashboard")
async def dashboard():
    try:
        user = await discord.fetch_user()

        # Request shared guilds from IPC
        get_user_admin_in_guilds = await ipc_client.request("get_shared_guilds", user=user.id)
        get_user_admin_in_guilds = (get_user_admin_in_guilds.response)

        # Check if the response is not None before accessing its attributes
        if get_user_admin_in_guilds is not None:
            guilds_as_admin = get_user_admin_in_guilds.get("admin_guilds", [])
        else:
            guilds_as_admin = []

        user_data = {
            "id": user.id,
            "username": user.name,
            "discriminator": user.discriminator,
            "avatar_url": str(user.avatar_url) if user.avatar_url else None
        }

        # Fetch guild information using IPC
        guild_infos = []
        guild_icons = []
        for server_id in guilds_as_admin:
            guild_info = await ipc_client.request("get_guild", guild_id=int(server_id))
            icon = guild_info.response.get("icon_url")
            guild_icons.append(icon)
            guild_infos.append(guild_info.response)

        # Include the user ID in the response
        return await render_template("server-select.html", username=user.name, user=user_data, admin_servers=guild_infos, guild_icons=guild_icons)

    except Unauthorized:
        return redirect(url_for("login"))


@app.route("/invite")
async def invite():
    return redirect("https://discord.com/api/oauth2/authorize?client_id=1137046154794774679&permissions=8&scope=bot")


@app.route("/support")
async def support():
    return redirect("https://discord.gg/ReSufm7r")


@app.route("/dashboard/<int:guild_id>")
async def server_dashboard(guild_id):
    try:
        user = await discord.fetch_user()
        get_user_admin_in_guilds = await ipc_client.request("get_shared_guilds", user=user.id)

        if get_user_admin_in_guilds.response is not None:
            guilds_as_admin = get_user_admin_in_guilds.response.get("admin_guilds", [])
        else:
            guilds_as_admin = []

        session["discord_user"] = {
            "id": user.id,
            "username": user.name,
            "discriminator": user.discriminator,
            "avatar_url": str(user.avatar_url) if user.avatar_url else None
        }

        guild_infos = []
        guild_icons = []

        for server_id in guilds_as_admin:
            guild_info = await ipc_client.request("get_guild", guild_id=int(server_id))
            icon = guild_info.response.get("icon_url")
            guild_icons.append({"id": server_id, "icon": icon})
            guild_infos.append(guild_info.response)

        selected_guild_info = next((info for info in guild_infos if info.get("id") == guild_id), None)
        selected_guild_icon = next((icon.get("icon") for icon in guild_icons if icon.get("id") == guild_id), None)

        return await render_template("dashboard.html", 
                                      username=user.name, 
                                      user=session["discord_user"], 
                                      guild_info=selected_guild_info, 
                                      selected_guild_icon=selected_guild_icon, 
                                      guild_icons=guild_icons)

    except Unauthorized:
        return redirect(url_for("login"))
    
@app.route("/roles/<int:guild_id>")
async def server_dashboard_roles(guild_id):
    try:
        user = await discord.fetch_user()
        get_user_admin_in_guilds = await ipc_client.request("get_shared_guilds", user=user.id)

        if get_user_admin_in_guilds.response is not None:
            guilds_as_admin = get_user_admin_in_guilds.response.get("admin_guilds", [])
        else:
            guilds_as_admin = []

        session["discord_user"] = {
            "id": user.id,
            "username": user.name,
            "discriminator": user.discriminator,
            "avatar_url": str(user.avatar_url) if user.avatar_url else None
        }

        guild_infos = []
        guild_icons = []

        for server_id in guilds_as_admin:
            guild_info = await ipc_client.request("get_guild", guild_id=int(server_id))
            icon = guild_info.response.get("icon_url")
            guild_icons.append({"id": server_id, "icon": icon})
            guild_infos.append(guild_info.response)

        selected_guild_info = next((info for info in guild_infos if info.get("id") == guild_id), None)
        selected_guild_icon = next((icon.get("icon") for icon in guild_icons if icon.get("id") == guild_id), None)

        # Fetch roles for the selected guild
        guild_roles_response = await ipc_client.request("get_guild_roles", guild_id=int(guild_id))

        # Check if the response is None or does not have the expected structure
        if guild_roles_response is None or 'roles' not in guild_roles_response.response:
            guild_roles = []
        else:
            guild_roles = guild_roles_response.response['roles']

        return await render_template("roles.html",
                                      username=user.name,
                                      user=session["discord_user"],
                                      guild_info=selected_guild_info,
                                      selected_guild_icon=selected_guild_icon,
                                      guild_icons=guild_icons,
                                      guild_roles=guild_roles)
    except Unauthorized:
        return redirect(url_for("login"))

@app.route("/feedback/<int:guild_id>")
async def server_dashboard_feedback(guild_id):
    try:
        user = await discord.fetch_user()
        get_user_admin_in_guilds = await ipc_client.request("get_shared_guilds", user=user.id)

        if get_user_admin_in_guilds.response is not None:
            guilds_as_admin = get_user_admin_in_guilds.response.get("admin_guilds", [])
        else:
            guilds_as_admin = []

        session["discord_user"] = {
            "id": user.id,
            "username": user.name,
            "discriminator": user.discriminator,
            "avatar_url": str(user.avatar_url) if user.avatar_url else None
        }

        guild_infos = []
        guild_icons = []

        for server_id in guilds_as_admin:
            guild_info = await ipc_client.request("get_guild", guild_id=int(server_id))
            icon = guild_info.response.get("icon_url")
            guild_icons.append({"id": server_id, "icon": icon})
            guild_infos.append(guild_info.response)

        selected_guild_info = next((info for info in guild_infos if info.get("id") == guild_id), None)
        selected_guild_icon = next((icon.get("icon") for icon in guild_icons if icon.get("id") == guild_id), None)

        # Fetch roles for the selected guild
        guild_roles_response = await ipc_client.request("get_guild_roles", guild_id=int(guild_id))

        # Check if the response is None or does not have the expected structure
        if guild_roles_response is None or 'roles' not in guild_roles_response.response:
            guild_roles = []
        else:
            guild_roles = guild_roles_response.response['roles']

        # Fetch channels for the selected guild
        guild_channels_response = await ipc_client.request("get_guild_channels", guild_id=int(guild_id))

        # Check if the response is None or does not have the expected structure
        if guild_channels_response is None or 'channels' not in guild_channels_response.response:
            guild_channels = []
        else:
            guild_channels = guild_channels_response.response['channels']

        return await render_template("feedback.html",
                                      username=user.name,
                                      user=session["discord_user"],
                                      guild_info=selected_guild_info,
                                      selected_guild_icon=selected_guild_icon,
                                      guild_icons=guild_icons,
                                      guild_roles=guild_roles,
                                      guild_channels=guild_channels)
    except Unauthorized:
        return redirect(url_for("login"))

    
@app.route("/test")
async def test():
    try:
        return await render_template('servers.html')
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

@app.route("/login")
async def login():
    return await discord.create_session()

@app.route("/callback/discord")
async def callback():
    try:
        await discord.callback()
        user = await discord.fetch_user()
        user_id = user.id  
        session["discord_user"] = {
            "id": user.id,
            "username": user.name,
            "discriminator": user.discriminator,
            "avatar_url": str(user.avatar.url) if user.avatar else None
        }
    except Exception as e:
        print(f"Callback error: {e}")
    return redirect(url_for("dashboard"))



@app.route("/save_roles", methods=['POST'])
async def save_roles():
    try:
        async with app.app_context():
            data = await request.json
            staff_roles = data.get("staff_roles")  # Use 'staff_roles' instead of 'roleIds'
            guild_id = data.get("guild_id")  # Add this line to get the guild ID from the request

            # Ensure that staff_roles is not None before processing
            if staff_roles is not None:
                # Process staff_roles and save to MongoDB or perform other actions
                # Also, include the guild_id in the request
                await ipc_client.request("save_staff_roles", guild_id=guild_id, staff_roles=staff_roles)

                return jsonify({"message": "success"})
            else:
                return jsonify({"error": "No staff_roles provided in the request"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})


@app.route("/save_management_roles", methods=['POST'])
async def save_management_roles():
    try:
        async with app.app_context():
            data = await request.json
            management_roles = data.get("management_roles")  
            guild_id = data.get("guild_id")  
            if management_roles is not None:
                await ipc_client.request("save_management_roles", guild_id=guild_id, management_roles=management_roles)

                return jsonify({"message": "success"})
            else:
                return jsonify({"error": "No management roles provided in the request"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})
    
    
@app.route("/save_hex", methods=['POST'])
async def save_hex():
    try:
        async with app.app_context():
            data = await request.json
            hex_value = data.get("hex_value")
            toggle_status = data.get("toggle_status")
            guild_id = data.get("guild_id")  

            if hex_value is not None:
                await ipc_client.request("save_hex", guild_id=guild_id, hex_value=hex_value, toggle_status=toggle_status)

                return jsonify({"message": "success"})
            else:
                return jsonify({"error": "No hex provided in the request"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})
    
@app.route("/save_nickname", methods=['POST'])
async def save_nickname():
    try:
        async with app.app_context():
            data = await request.json
            nickname_value = data.get("nickname_value")
            toggle_status = data.get("toggle_status")# Use 'staff_roles' instead of 'roleIds'
            guild_id = data.get("guild_id")  # Add this line to get the guild ID from the request

            # Ensure that staff_roles is not None before processing
            if nickname_value is not None:
                await ipc_client.request("save_nickname", guild_id=guild_id, nickname_value=nickname_value, toggle_status=toggle_status)

                return jsonify({"message": "success"})
            else:
                return jsonify({"error": "No staff_roles provided in the request"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})
    
@app.route("/save_prefix", methods=['POST'])
async def save_prefix():
    try:
        async with app.app_context():
            data = await request.json
            bot_prefix = data.get("bot_prefix")
            guild_id = data.get("guild_id")  
            if bot_prefix is not None:
                await ipc_client.request("save_prefix", guild_id=guild_id, bot_prefix=bot_prefix)

                return jsonify({"message": "success"})
            else:
                return jsonify({"error": "No prefix provided in the request"})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)