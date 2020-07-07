const form = document.querySelector('form')
const usernameElt = form.username
const emailElt = form.email
const passwordElt = form.password1
const password2Elt = form.password2
const fields = [usernameElt, emailElt, passwordElt, password2Elt]

const throwError = (elt, message) => {
    const prt = elt.parentNode
    try {
        prt.removeChild(prt.querySelector('.error'))
    } catch (e) {
        console.log(e)
    }
    const msgPara =  document.createElement('p')
    msgPara.textContent = message
    msgPara.classList.add('error')
    prt.classList.add('error-field')

    prt.appendChild(msgPara)
}

const emailVerifie = (email) => {
    const emailRegex = /^[a-z0-9._\-+%]+\@[a-z]+\.[a-z]{2,}$/g
    if (emailRegex.test(email)) return true
    else throwError(emailElt, 'Invalid email address.')
    return false
}

const usernameVerifie = (username) => {
    const usernameRegex = /^[A-Z]?[a-z]+[0-9]*$/g

    if(username.length < 6) {
        throwError(usernameElt, 'Username must contain more than 5 characteres.')
    } else if(/[\W]/.test(username)) {
        throwError(usernameElt, 'Username must contain only letters numbers and underscores.')
    } else if(!usernameRegex.test(username)) {
        throwError(usernameElt, 'Username must start with a letter and contain only letters numbers or underscore.')
    } else {
        return true
    }
    return false
}

const passwordVerifie = (password) => {
    if(password.length < 8 || !(/[A-Z]+/.test(password) && /[a-z]+/.test(password) && /[0-9]+/.test(password))) {
        throwError(passwordElt, 'Password must be min. 8 characters. combine numbers upper and lowercase letters.') 
    } else {
        return true
    }
    return false
}

const passwordsCompare = (password1, password2) => {
    if(password1 !== password2) {
        throwError(password2Elt, 'Password does not match.')
    } else {
        return true
    }
    return false
}

const validateForm = (e) => {
    const username = usernameElt.value
    const email = emailElt.value
    const password = passwordElt.value
    const password2 = password2Elt.value
    
    const usernameVerified = usernameVerifie(username)
    const emailVerified = emailVerifie(email)
    const passwordVerified = passwordVerifie(password)
    const password2Verified = passwordsCompare(password, password2)

    if(!usernameVerified || !emailVerified || !passwordVerified || !password2Verified) {
        e.preventDefault()
    }

}

const removeError = (e) => {
    const prt = e.target.parentNode
    try {
        prt.removeChild(prt.querySelector('.error'))
    } catch (e) {
        console.log(e)
    }
    prt.classList.remove('error-field')
}

form.addEventListener("submit", validateForm)
fields.forEach(field => field.addEventListener('input', removeError))