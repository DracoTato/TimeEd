function sendEmail() {
    const textArea = document.querySelector("#email-subject")
    const email = document.querySelector("#email").getAttribute("href")
    let subject = "About TimeED"
    let body = textArea.value
    window.open(`${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`)

}