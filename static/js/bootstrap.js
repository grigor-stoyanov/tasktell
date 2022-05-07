document.addEventListener('DOMContentLoaded', () => {
to_destroy = document.querySelectorAll(" a[href^='#tsk']")
    for (let i = 1; i < to_destroy.length; i += 2) {
        to_destroy[i].remove()
    }
})
