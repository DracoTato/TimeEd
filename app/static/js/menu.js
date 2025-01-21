function toggleMenu() {
    const links = document.querySelector(".nav-links");
    const hamMenu = document.querySelector(".hamburger-menu")
    if (links.style.display == "") {
    links.style.display = "block";
    hamMenu.classList.add("active")
    } else {
        links.style.display = "";
        hamMenu.classList.remove("active")
    }
}

function handleKey(e) {
    if (e.key === "Enter" || e.key === ' ') {
        toggleMenu()
    } 
}
