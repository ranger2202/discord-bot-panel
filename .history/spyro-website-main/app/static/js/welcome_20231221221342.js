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
    const toggleCheckbox = document.getElementById('botFeedbackToggle');

    if (toggleCheckbox.checked) {
        showCustomAlert('Toggled!!');
    }
    else {
        showCustomBadAlert('uqwfqwfqwmtgew')
    }
}

