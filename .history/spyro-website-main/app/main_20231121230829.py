# main.py
from quart import Quart, send_file, redirect, url_for, render_template
from discord.ext.ipc import Client
from quart_discord import DiscordOAuth2Session, requires_authorization
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Quart(__name__)
app.config["SECRET_KEY"] = "2424242424"
app.config["DISCORD_CLIENT_ID"] = 1102601502851354716
app.config["DISCORD_CLIENT_SECRET"] = "fF94icJfSEDNFjP_8G5FuPcQ8iVXlrEL"
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:8000/callback"

ipc = Client(host="bot ip.", secret_key="SuperSecretKey", standard_port=5000, multicast_port=5001)
discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
    return await render_template("template.html")

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

if __name__ == "__main__":
    app.run(debug=True, port=8000)