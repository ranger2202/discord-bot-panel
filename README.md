# Discord Bot Panel
### A simple project that allows you to use the web to start, stop, and make commands for your discord bot

## Create a project
view the steps below to successfully set the project up.

```py

# Clone the github repository into your IDE 
git clone https://github.com/ranger2202/discord-bot-panel.git

# cd into your directory
cd path-to-directory

# Installing the required dependencies 
pip install -r requirements.txt
```

## Developing
Once you've created the project and installed the correct dependencies, start testing the project.

```py

# bind the website
hypercorn run:app --bind localhost:8000

# or start the website through the file
python3 run.py

```


### Once you've followed all of these steps you have successfully started the project.