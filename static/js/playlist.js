const editTitleBtn = document.getElementById('edit-title')
const playlistTitleDiv = document.getElementById('playlist-title')
const privacyInput = document.getElementById('privacy-input')
const removeBtns = document.querySelectorAll('.playlist-items .video .remove-video')

const savePlaylistTitle = async (e) => {
    const playlistId = e.target.getAttribute('data-id')
    const playlistNewTitle = e.target.value
    const data = {'id': playlistId, 'title': playlistNewTitle}

    const req = await fetch('/playlist', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })

    if(req.status >= 200 && req.status < 300) {
        const titleElt = document.createElement('h6')
        titleElt.textContent = playlistNewTitle
        playlistTitleDiv.replaceChild(titleElt, e.target)
        editTitleBtn.classList.remove('hide')
    }
} 

const setPrivacy = async  (e) => {
    const is_private = e.target.checked
    const id = e.target.getAttribute('data-id')
    const data = {'id': id, 'privacy': is_private}

    const req = await fetch('/playlist', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
}

const editTitle = (e) => {
    const playlistId = e.target.getAttribute('data-id') || e.target.parentNode.getAttribute('data-id') 
    const playlistTitle = playlistTitleDiv.querySelector('h6').textContent 
    const titleInput = document.createElement('input')
    titleInput.type = 'text'
    titleInput.value = playlistTitle
    titleInput.setAttribute('data-id', playlistId)
    playlistTitleDiv.replaceChild(titleInput, playlistTitleDiv.querySelector('h6'))
    titleInput.select()
    titleInput.focus()
    titleInput.addEventListener('blur', savePlaylistTitle)
    
    if(e.target.hasAttribute('data-id')) e.target.classList.add('hide')
    else  e.target.parentNode.classList.add('hide')
}

const removePlaylist = async e => {
    const id = e.target.getAttribute('data-id') || e.target.parentNode.getAttribute('data-id')
    const playlistId = e.target.getAttribute('data-playlist') || e.target.parentNode.getAttribute('data-playlist')
    const action = -1
    const data = {'videoId': id, 'playlistId': playlistId, 'action': action}

    const req = await fetch('/api/playlists', {
        method: 'PUT',
        body: JSON.stringify(data),
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })

    if(req.status >= 200 && req.status < 300) {
        const target = document.getElementById(id)
        target.parentNode.removeChild(target)
    }
}

if (editTitleBtn) {
    editTitleBtn.addEventListener('click', editTitle)
}

if(privacyInput) {
    privacyInput.addEventListener('change', setPrivacy)
}

removeBtns.forEach(btn =>  btn.addEventListener('click', removePlaylist))