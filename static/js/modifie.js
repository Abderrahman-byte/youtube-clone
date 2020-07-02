const posterInput = document.getElementById('video-poster-input')
const poster = document.getElementById('video-poster')

const loadPoster = e => {
    const data = e.target.result

    if(data !== null) {
        poster.setAttribute('src', data)
    }
}

const updatePoster = e => {
    const file = e.target.files[0]
    const reader = new FileReader()

    reader.addEventListener('loadend', loadPoster)
    reader.readAsDataURL(file)
}
posterInput.addEventListener('input', updatePoster)