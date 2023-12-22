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

function updateServerColor() {
    var hexColor = document.getElementById("serverColorInput").value;

    if (/^#[0-9A-Fa-f]{6}$/i.test(hexColor)) {
        var colorCircle = document.getElementById("colorCircle");
        colorCircle.style.backgroundColor = hexColor;
        colorCircle.style.display = 'flex';
    } else {
        document.getElementById("colorCircle").style.display = 'none';
    }
}

document.getElementById("serverColorInput").addEventListener("input", updateServerColor);

function toggleBotColors() {
    const toggleCheckbox = document.getElementById('botColorToggle');
    const hexInput = document.getElementById('serverColorInput');

    if (toggleCheckbox.checked) {
        showCustomAlert('test!!');
    } else {
        showCustomBadAlert('Not Toggled!!');
    }
}
function saveHex() {
    var hexValue = document.getElementById("serverColorInput").value;
    var toggleValue = document.getElementById('botColorToggle').checked ? 1 : 0;
    showCustomAlert('Hex and toggle status saved successfully');
    if (/^[0-9A-Fa-f]{6}$/i.test(hexValue)) {
        var guildId = document.getElementById("guild_id").value;

        fetch('/save_hex', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ guild_id: guildId, hex_value: hexValue, toggle_status: toggleValue }),
        })
            .then(response => response.json())
            .then(data => {
                showCustomAlert('Hex and toggle status saved successfully');
            })
            .catch(error => {
                showCustomBadAlert('There was an error saving the hex and toggle status.');
            });
    } else {
        showCustomBadAlert('Invalid hex color code. Please enter a valid color code.');
    }
}

document.getElementById("saveButton").addEventListener("click", saveHex);
