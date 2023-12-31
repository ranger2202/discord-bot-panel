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