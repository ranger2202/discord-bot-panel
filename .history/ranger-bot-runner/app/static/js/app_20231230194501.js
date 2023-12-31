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


function makeCommand() {
    var commandName = document.getElementById('commandName').value;
    var commandResponse = document.getElementById('commandResponse').value;

    if (commandName && commandResponse) {
        fetch('/addcommands', { // Adjusted to match the server route
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
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error somewhere.');
        });
    } else {
        alert('Please fill in both fields.');
    }
}