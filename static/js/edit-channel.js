const profilImg = document.getElementById('profil-img')
const backgroundImg = document.getElementById('background-img')
const wallpaper = document.getElementById('wallpaper')
const profil = document.getElementById('profil')
const alertBackboard = document.getElementById('alert-backboard')
const alertDisplay = document.getElementById('alert-display')
const closeAlertBtn = document.getElementById('close-alert')
const alertText = document.getElementById('alert-text')
const aboutArea = document.getElementById('about-area')
const aboutInput = document.getElementById('about')

const closeAlert = () => {
    alertBackboard.style.display = 'none'
    alertDisplay.style.display = 'none'
}

const showAlert = (Text) => {
    alertText.textContent = Text
    alertBackboard.style.display = 'block'
    alertDisplay.style.display = 'flex'
}

const changeImg = (e, target, minWidth, minHeight, d) => {
    const file = e.target.files[0]
    
    const reader = new FileReader()
    const img = new Image()

    reader.addEventListener('loadend', (e) => {
        const data = e.target.result
        img.src = data
    })

    img.addEventListener('load', () => {
        if(img.width >= minWidth && img.height >= minHeight) {
            target.style.backgroundImage = `url('${reader.result}')`
        } else {
            e.target.files = (new DataTransfer()).files
            target.style.backgroundImage = `url('${target.getAttribute('data-default')}')`
            showAlert(`Image dimensions required are : ${minWidth} x ${minHeight}`)
        }
    })

    reader.readAsDataURL(file)
}

backgroundImg.addEventListener('change', e => {
    changeImg(e, wallpaper, 1200, 200)
})

profilImg.addEventListener('change', e => {
    changeImg(e, profil, 300, 300)
})

alertBackboard.addEventListener('click', closeAlert)
closeAlertBtn.addEventListener('click', closeAlert)
aboutArea.addEventListener('input', (e) => aboutInput.value= e.target.value)