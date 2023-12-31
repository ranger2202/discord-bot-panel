function startBot() {
  var token = document.getElementById('token').value;
  fetch('/start_bot', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ bot_token: token }),  // Adjusted to match server expectation
  })
  .then(response => response.json())
  .then(data => {
      alert(data.message);  // Display the server response message
  })
  .catch(error => {
      alert('There was an error somewhere.');
  });
}


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
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error stopping the bot.');
    });
}



function makeCommand() {
    // Check if the bot is running by sending a request to a new endpoint
    fetch('/check_bot_status')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'running') {
                // Bot is running, proceed to add command
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
