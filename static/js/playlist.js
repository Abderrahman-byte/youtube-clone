const editTitleBtn = document.getElementById('edit-title')
const playlistTitleDiv = document.getElementById('playlist-title')

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

if (editTitleBtn) {
    editTitleBtn.addEventListener('click', editTitle)
}