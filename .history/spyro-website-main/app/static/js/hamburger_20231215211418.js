function toggleMenu() {
  var navList = document.querySelector('.nav-list');
  navList.classList.toggle('show');
}

function dropdown() {
  var dropdownContent = document.getElementById('myDropdown');
  dropdownContent.classList.toggle('show');
}

document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.querySelector('.hamburger');
  const navList = document.querySelector('.nav-list');
  const dropdownButton = document.querySelector('.dropbtn');

  hamburger.addEventListener('click', function () {
      navList.classList.toggle('show');
  });

  dropdownButton.addEventListener('click', function () {
      dropdown();
  });
});