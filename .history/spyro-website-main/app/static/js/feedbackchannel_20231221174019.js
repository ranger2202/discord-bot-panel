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

function saveRoles1() {
    var selectedRoles = document.getElementById("rolesDropdown1").selectedOptions;

    if (selectedRoles.length === 0) {
        showCustomBadAlert('Please select a role before saving.');
        return;
    }

    var roleIds = [];
    var guildId = document.getElementById("guild_id").value;

    for (var i = 0; i < selectedRoles.length; i++) {
        var roleId = selectedRoles[i].value;
        roleIds.push(roleId);
    }

    fetch('/save_management_roles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ guild_id: guildId, management_roles: roleIds }),  
    })
    .then(response => response.json())
    .then(data => {
        showCustomAlert('Channel saved successfully');
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

function saveToggle() {
    var hexValue = document.getElementById("serverColorInput").value;
    var toggleValue = document.getElementById('botColorToggle').checked ? 1 : 0;

    if (/^#[0-9A-Fa-f]{6}$/i.test(hexValue)) {
        var guildId = document.getElementById("guild_id").value;

        fetch('/save_toggle_feedback', {
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

document.getElementById("saveToggle").addEventListener("click", saveToggle);
