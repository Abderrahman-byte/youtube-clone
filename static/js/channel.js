const authDisplay = document.getElementById('auth-display')
const authBackboard = document.getElementById('auth-blackboard')
const closeAuthDisplayBtn = document.getElementById('close-auth')

const getCookie = name => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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