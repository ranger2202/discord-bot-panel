document.addEventListener("DOMContentLoaded", function () {
  var hamburger = document.querySelector('.hamburger');
  var navList = document.querySelector('.nav-list');

  hamburger.addEventListener('click', function () {
      navList.style.display = (navList.style.display === 'flex') ? 'none' : 'flex';
  });
});
