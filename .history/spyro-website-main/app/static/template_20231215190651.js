function toggleMenu() {
    var navList = document.querySelector(".nav-list");
    if (navList.style.display === "none" || navList.style.display === "") {
      navList.style.display = "flex";
    } else {
      navList.style.display = "none";
    }
  }