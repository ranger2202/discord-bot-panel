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


function toggleBotNickname() {
    const toggleCheckbox = document.getElementById('botNickToggle');
    const nickInput = document.getElementById('serverNicknameInput');

    if (toggleCheckbox.checked) {
        showCustomAlert('Toggsdgsgled!!');
    } else {
        showCustomBadAlert('Not Toggled!!');
    }
}
function saveNickname() {
    var nicknameValue = document.getElementById("serverNicknameInput").value;
    var toggleValue = document.getElementById('botNickToggle').checked ? 1 : 0;
    if (nicknameValue.trim() === '') {
        showCustomBadAlert('Please type something before saving.');
        return; 
    }
    var guildId = document.getElementById("guild_id").value;

    fetch('/save_nickname', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ guild_id: guildId, nickname_value: nicknameValue, toggle_status: toggleValue}),
    })
        .then(response => response.json())
        .then(data => {
            showCustomAlert('Nickname and toggle status saved successfully');
        })
        .catch(error => {
            showCustomBadAlert('There was an error saving the hex and toggle status.');
        });
} 

document.getElementById("saveButton1").addEventListener("click", saveNickname);
