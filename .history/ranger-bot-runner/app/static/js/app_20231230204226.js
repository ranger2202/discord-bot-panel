// Function to check if the bot is running
function isBotRunning() {
    return fetch('/check_bot_status')
        .then(response => response.json())
        .then(data => data.status === 'running')
        .catch(error => {
            console.error('Error:', error);
            return false;
        });
}

// Function to update button visibility
function updateButtonVisibility() {
    const startButtonContainer = document.getElementById("startButtonContainer");
    const stopButtonContainer = document.getElementById("stopButtonContainer");

    isBotRunning().then(botRunning => {
        if (botRunning) {
            startButtonContainer.style.display = "none";
            stopButtonContainer.style.display = "block";
        } else {
            startButtonContainer.style.display = "block";
            stopButtonContainer.style.display = "none";
        }
    });
}

// Function to start the bot
// Function to start the bot
function startBot() {
    var token = document.getElementById('token').value;
    fetch('/start_bot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ bot_token: token }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error somewhere.');
    });
}


// Function to stop the bot
function stopBot() {
    fetch('/stop_bot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || 'Bot stopped successfully');
        updateButtonVisibility();  // Update button visibility after stopping the bot
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error stopping the bot.');
    });
}

// Function to add a custom command
function makeCommand() {
    isBotRunning().then(botRunning => {
        if (botRunning) {
            var commandName = document.getElementById('commandName').value;
            var commandResponse = document.getElementById('commandResponse').value;

            if (commandName && commandResponse) {
                fetch('/addcommands', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        commands_list: [{ command_name: commandName, response: commandResponse }],
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message || 'Custom command added successfully');
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('There was an error somewhere.');
                });
            } else {
                alert('Please fill in both fields.');
            }
        } else {
            alert('The bot is not currently running. Start the bot before adding commands.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error checking the bot status.');
    });
}

// Call the function to set initial button visibility
updateButtonVisibility();
