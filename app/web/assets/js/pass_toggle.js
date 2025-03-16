let eyes = document.querySelectorAll(".pass-toggle");
let passwords = document.querySelectorAll("input[type='password']");

eyes.forEach((eye) => {
  eye.addEventListener("click", (e) => {
    e.preventDefault();
    eye.classList.toggle("on");
    const password = passwords[Array.from(eyes).indexOf(eye)];
    password.type = password.type === "password" ? "text" : "password";
  });
});
