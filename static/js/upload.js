const videoInput = document.getElementById('video_input')
const videoLabel = document.querySelector('.upload_form > label')
const submitBtn =  document.querySelector('.upload_form > button')

const reader = new FileReader()

const uplaodFile = e => {
    const file = e.target.files[0]
    const reader = new FileReader()

    reader.addEventListener('loadend', () => {
        const data = reader.result
        if(data !== null ) {
            videoLabel.style.display = 'none'
            submitBtn.style.display = 'block'
            video.setAttribute('src', data)
            videoContainer.classList.remove('hidden')
        }
    })

    reader.readAsDataURL(file)
}

videoInput.addEventListener('change', uplaodFile)