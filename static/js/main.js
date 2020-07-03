const backboard = document.getElementById('backboard')
const navCloser = document.getElementById('hide_nav')
const nav = document.getElementById('nav')
const navBars = document.getElementById('nav_bars')

const hideNav = () => {
    nav.classList.remove('show')
    backboard.style.display = 'none'
}

const showNav = () => {
    nav.classList.add('show')
    backboard.style.display = 'block'
}

navCloser.addEventListener('click', hideNav)
backboard.addEventListener('click', hideNav)
navBars.addEventListener('click', showNav)