// sidebar.js

function toggleSidebarDropdown() {
    var dropdownContent = document.querySelector('.sidebar-dropdown-content');
    var dropdownImage = document.getElementById('sidebarDropdownImage');

    if (dropdownContent.style.display === 'block') {
        dropdownContent.style.display = 'none';
        dropdownImage.src = "./../static/images/downarrowwavey.png";
    } else {
        dropdownContent.style.display = 'block';
        dropdownImage.src = "./../static/images/uparrowwavey.png";
    }
}
