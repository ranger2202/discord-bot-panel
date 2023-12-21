function toggleRolesDropdown() {
    var dropdown = document.getElementById("rolesDropdown");
    dropdown.classList.toggle("show");

    var arrowImage = document.getElementById('dropdownImage');
    if (dropdown.classList.contains("show")) {
        arrowImage.src = './../static/images/uparrowwavey.png'; 
    } else {
        arrowImage.src = './../static/images/downarrowwavey.png'; 
    }
}

function selectRole(roleId) {
    var selectedRoles = document.getElementById("rolesDropdown").selectedOptions;
    var selectorContainor = document.querySelector(".selector-containor");
    
  
    selectorContainor.innerHTML = "";
    var arrowImage = document.getElementById('dropdownImage');
    if (dropdown.classList.contains("show")) {
        arrowImage.src = './../static/images/uparrowwavey.png'; 
    } else {
        arrowImage.src = './../static/images/downarrowwavey.png';
    }   
    for (var i = 0; i < selectedRoles.length; i++) {
        var selectedRole = selectedRoles[i].text;

        // Create a new element to display the selected role
        var roleElement = document.createElement("div");
        roleElement.classList.add("selected-role");
        roleElement.innerText = selectedRole;

        selectorContainor.appendChild(roleElement);
    }
    
    toggleRolesDropdown();
}
function handleRoleSelection() {
    var selectedRoles = document.getElementById("rolesDropdown").selectedOptions;
    var selectorContainor = document.querySelector(".selector-containor");

    selectorContainor.innerHTML = "";

    for (var i = 0; i < selectedRoles.length; i++) {
        var selectedRole = selectedRoles[i].text;

        var roleElement = document.createElement("div");
        roleElement.classList.add("selected-role-box");
        roleElement.innerText = selectedRole;

        selectorContainor.appendChild(roleElement);
    }

    // Close the dropdown
    toggleRolesDropdown();
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

function saveRoles() {
    var selectedRoles = document.getElementById("rolesDropdown").selectedOptions;

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

    fetch('/save_roles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ guild_id: guildId, staff_roles: roleIds }), 
    })
    .then(response => response.json())
    .then(data => {
        showCustomAlert('Roles saved successfully');
    })
    .catch(error => {
        showCustomBadAlert('There was an error saving the roles.');
    });
}
