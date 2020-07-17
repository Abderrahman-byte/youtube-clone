const authDisplay = document.getElementById('auth-display')
const authBackboard = document.getElementById('auth-blackboard')
const closeAuthDisplayBtn = document.getElementById('close-auth')

const closeAuthDisplay = () => {
    authDisplay.style.display = 'none'
    authBackboard.style.display =  'none'
}

const showAuthDisplay = () => {
    authDisplay.style.display = 'flex'
    authBackboard.style.display =  'block'
}

authBackboard.addEventListener('click', closeAuthDisplay)
closeAuthDisplayBtn.addEventListener('click', closeAuthDisplay)