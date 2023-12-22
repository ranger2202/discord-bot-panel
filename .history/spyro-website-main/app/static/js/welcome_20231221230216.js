function showCustomAlert(message) {
    var alertContainer = document.getElementById("alertContainer");
    alertContainer.innerText = message;
    alertContainer.style.display = "block";

    setTimeout(function () {
        alertContainer.style.display = "none";
    }, 5000);
}
function showCustomBadAlert(message) {
    var alertContainer = document.getElementById("alertBadContainer");
    alertContainer.innerText = message;
    alertContainer.style.display = "block";

    setTimeout(function () {
        alertContainer.style.display = "none";
    }, 5000);
}

function toggleFeedback() {
    console.log('Function called!'); 
    const toggleCheckbox = document.getElementById('botWelcomeToggle');

    if (toggleCheckbox.checked) {
        showCustomAlert('Toggled!!');
    }
    else {
        showCustomBadAlert('uqwfqwfqwmtgew')
    }
}


function saveChannel() {
    var selectedChannel = document.getElementById("rolesDropdown1").selectedOptions;
    var selectedRole = document.getElementById("welcom-dropdown").selectedOptions;
    var welcomeMessage = document.getElementById("welcomeMessageInput").value;
    var toggleValue = document.getElementById('botWelcomeToggle').checked ? 1 : 0;
    if (selectedChannel.length === 0 || selectedChannel[0].value === "") {
        showCustomBadAlert('Please select a channel before saving.');
        return;
    }
    if (selectedRole.length === 0 || selectedRole[0].value === "") {
        showCustomBadAlert('Please select a role before saving.');
        return;
    }
    if (welcomeMessage.trim() === '') {
        showCustomBadAlert('Please type a welcome message before saving.');
        return; 
    }
    var channelId = selectedChannel[0].value;
    var rolelId = selectedRole[0].value; // Access the value of the first selected option
    var guildId = document.getElementById("guild_id").value;

    fetch('/save_welcome', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ guild_id: guildId, feedback_channel: channelId, toggle_status: toggleValue }),  
    })
    .then(response => response.json())
    .then(data => {
        showCustomAlert('Channel saved successfully');
    })
    .catch(error => {
        showCustomBadAlert('There was an error saving the roles.');
    });
}

