function toggleRolesDropdown1() {
    var dropdown = document.getElementById("rolesDropdown1");
    dropdown.classList.toggle("show");

    var arrowImage = document.getElementById('dropdownImage-1');
    if (dropdown.classList.contains("show")) {
        arrowImage.src = './../static/images/uparrowwavey.png'; 
    } else {
        arrowImage.src = './../static/images/downarrowwavey.png'; 
    }
}

function selectRole1(roleId) {
    var selectedRoles = document.getElementById("rolesDropdown1").selectedOptions;
    var selectorContainor = document.querySelector(".selector-containor-1");
    
    selectorContainor.innerHTML = "";
    var arrowImage = document.getElementById('dropdownImage-1');
    if (dropdown.classList.contains("show")) {
        arrowImage.src = './../static/images/uparrowwavey.png';
    } else {
        arrowImage.src = './../static/images/downarrowwavey.png'; 
    }   
    for (var i = 0; i < selectedRoles.length; i++) {
        var selectedRole = selectedRoles[i].text;

        var roleElement = document.createElement("div");
        roleElement.classList.add("selected-role");
        roleElement.innerText = selectedRole;

        selectorContainor.appendChild(roleElement);
    }
    
    toggleRolesDropdown1();
}
function handleRoleSelection1() {
    var selectedRoles = document.getElementById("rolesDropdown1").selectedOptions;
    var selectorContainor = document.querySelector(".selector-containor-1");

    selectorContainor.innerHTML = "";

    for (var i = 0; i < selectedRoles.length; i++) {
        var selectedRole = selectedRoles[i].text;

        var roleElement = document.createElement("div");
        roleElement.classList.add("selected-role-1");
        roleElement.innerText = selectedRole;

        selectorContainor.appendChild(roleElement);

        if (i < selectedRoles.length - 1) {
            selectorContainor.appendChild(document.createTextNode(', '));
        }
    }


    toggleRolesDropdown1();
}
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
function saveChannel() {
    var selectedChannel = document.getElementById("rolesDropdown1");
    var toggleValue = document.getElementById('botColorToggle').checked ? 1 : 0;
    if (selectedChannel.length === 0) {
        showCustomBadAlert('Please select a channel before saving.');
        return;
    }

    var channelId = selectedChannel; // Access the value of the first selected option
    var guildId = document.getElementById("guild_id").value;

    fetch('/save_feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ guild_id: guildId, feedback_channel: channelId, toggle_status: toggleValue }),  
    })
    .then(response => response.json())
    .then(data => {
        showCustomAlert('Channel saved successfully', toggleValue, channelId);
    })
    .catch(error => {
        showCustomBadAlert('There was an error saving the roles.');
    });
}






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
