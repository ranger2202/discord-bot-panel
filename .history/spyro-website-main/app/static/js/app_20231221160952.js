function dropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }


  if(window.innerWidth >= 640){
    nav.style.height = "4.3125rem"
    // h1.forEach(e=>{
    //     e.style.fontSize = "5vw"
    // })   
    navBtn.style.display = "none"
}
if(window.innerWidth < 640){
    nav.style.height = "2rem"
    nav.style.paddingLeft = "1.8rem"
    nav.style.paddingBottom = "2rem"
    li.style.display = "none"
    // h1.forEach(e=>{
    //     e.style.fontSize = "12vw"
    // })   
}
function clicking(){
    navBtn.addEventListener('click', ()=>{
        li.style.display = "grid"
        nav.style.height = "16rem"
        
        navBtn.addEventListener('click', ()=>{
            li.style.display = "none"
            nav.style.height = "2rem"
            clicking()
        })
    })
}
clicking()