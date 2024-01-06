const yearSpan = document.body.querySelector(".current-year")

if (yearSpan) {
    const currentDate = new Date()
    yearSpan.innerHTML = currentDate.getFullYear()
}