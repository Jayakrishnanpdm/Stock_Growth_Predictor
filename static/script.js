let burger_icon = document.querySelector('.burger-icon');
let ul = document.querySelector("nav ul");
burger_icon.addEventListener("click",()=>{
    ul.classList.toggle("active");
})


function gotosecondpage() {
        window.location.replace('/search') // Redirect to page2.html
}