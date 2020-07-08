const video_ = document.getElementById('video')
const impressionBtns = [document.getElementById('like-btn'), document.getElementById('dislike-btn')]
const impressionCounts = [document.getElementById('likes-count'), document.getElementById('dislikes-count')]
const saveBtn = document.getElementById('save-playlist')
const playlistsBlackBoard = document.getElementById('playlists-blackboard')
const playlistsDisplay = document.getElementById('playlists-container')
const playlistContainer = document.getElementById('playlists')
const closePlaylistsBtn = document.getElementById('close-playlists')
const createPlaylistBtn = document.getElementById('create-playlist')
const createPlaylistForm = document.getElementById('playlist-form')
const playlistFormError = document.querySelector('.playlist-form .error')

const formatCount = count => {
    if (count < 0) {
        return 0
    }

    const md = Math.floor(count / 1000000000)
    const m = Math.floor((count - (md * 1000000000)) / 1000000)
    const k = Math.floor((count - (md * 1000000000) - (m * 1000000)) / 1000)
    const u = Math.floor(count - (md * 1000000000) - (m * 1000000) - (m * 1000))

    if (md > 0) {
        return `${md}Md`
    } else if (m > 0) {
        return `${m}M`
    } else if (k > 0) {
        return `${k}k`
    } else {
        return u
    }
}

const updateImpressionsCount = () => {
    impressionCounts.forEach(elt => {
        const count = parseInt(elt.dataset.count, 10) || 0
        elt.textContent = formatCount(count)
    })
}

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

const submitImpression = async e => {
    const target = impressionBtns.includes(e.target) ? e.target : e.target.parentNode
    const method = target.classList.contains('active') ? 'DELETE' : 'POST'
    const action = target.getAttribute('data-action') || '1'
    const id = video_.getAttribute('data-id')

    if (method === 'POST') {
        const data = { 'id': id, 'kind': action }
        const req = await fetch('/api/impression', {
            'method': 'POST',
            'body': JSON.stringify(data),
            'headers': {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })

        if (req.status >= 200 && req.status < 300) {
            impressionBtns.forEach(btn => {
                if (btn.classList.contains('active')) {
                    btn.nextElementSibling.setAttribute('data-count',
                        parseInt(btn.nextElementSibling.getAttribute('data-count'), 10) - 1)
                }
            })

            impressionBtns.forEach(btn => btn.classList.remove('active'))
            target.nextElementSibling.setAttribute('data-count',
                parseInt(target.nextElementSibling.getAttribute('data-count'), 10) + 1)
            target.classList.add('active')
            updateImpressionsCount()
        }
    } else if (method === 'DELETE') {
        const data = { 'id': id }
        const req = await fetch('/api/impression', {
            'method': 'DELETE',
            'body': JSON.stringify(data),
            'headers': {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })

        if (req.status >= 200 && req.status < 300) {
            const sib = target.nextElementSibling
            const count = parseInt(sib.getAttribute('data-count'), 10) || 0
            sib.setAttribute('data-count', count - 1)
            updateImpressionsCount()
            console.log(count)
            impressionBtns.forEach(btn => btn.classList.remove('active'))
        }
    }
}

const editPlaylist = async e => {
    const action = e.target.checked ? 1 : -1
    const videoId = video_.getAttribute('data-id')
    const playlistId = e.target.getAttribute('data-id')

    const data = {'videoId': videoId, 'playlistId': playlistId, 'action': action}
    const req = await fetch('/api/playlists', {
        'method': 'PUT',
        'body': JSON.stringify(data),
        'headers': {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
}

const saveVideo = async () => {
    const req = await fetch('/api/playlists')

    if (req.status >= 200 && req.status < 300) {
        const videoId = video_.getAttribute('data-id')
        const res = await req.json()
        const playlists = res.playlists
        playlistContainer.innerHTML = ''

        playlists.forEach(pl => {
            const html = `<label class="item">${pl.title}
                <input class="playlist-checkbox" type="checkbox" data-id="${pl.id}" ${pl.items.includes(videoId) ? 'checked': ''}>
                <span class="checkmark"></span>
                ${pl.is_public? '<i class="fas fa-globe"></i>': '<i class="fas fa-lock"></i>'}
            </label>`
            playlistContainer.innerHTML += html
        })

        const plsCheckboxes = document.querySelectorAll('.playlist-checkbox')
        plsCheckboxes.forEach(cb => cb.addEventListener('change', editPlaylist))
        playlistsDisplay.style.display = 'block'
        playlistsBlackBoard.style.display = 'block'
    }
}

const closePlaylistsDisplay = () => {
    playlistsDisplay.style.display = 'none'
    playlistsBlackBoard.style.display = 'none'
    createPlaylistForm.style.display = 'none'
    playlistFormError.style.display = 'none'
    createPlaylistBtn.style.display = 'block'
    createPlaylistForm.reset()
    playlistContainer.innerHTML = ''
}

const showPlaylistForm = () => {
    createPlaylistForm.style.display = 'flex'
    createPlaylistBtn.style.display = 'none'
}

const createPlaylist = async e => {
    e.preventDefault()
    const title = e.target.title.value
    const privacy = e.target.privacy.checked
    const videoId = video_.getAttribute('data-id')
    const data = {title, privacy, videoId}

    const req = await fetch('/api/playlists', {
        method: 'POST',
        body: JSON.stringify(data),
        headers : {
            'X-CSRFToken': getCookie('csrftoken') 
        }
    })

    if(req.status >= 200 && req.status < 300) {
        const pl = await req.json()
        const html = `<label class="item">${title}
                <input class="playlist-checkbox" type="checkbox" data-id="${pl.id}" checked>
                <span class="checkmark"></span>
                ${privacy? '<i class="fas fa-lock"></i>': '<i class="fas fa-globe"></i>'}
            </label>`
        playlistContainer.innerHTML += html
        createPlaylistForm.reset()
        createPlaylistForm.style.display = 'none'
        createPlaylistBtn.style.display = 'block'
    } else {
        const msg = await req.text()
        playlistFormError.textContent = msg
        playlistFormError.style.display = 'block'

        setTimeout(() => playlistFormError.style.display = 'none', 3000)
    }
}

saveBtn.addEventListener('click', saveVideo)
closePlaylistsBtn.addEventListener('click', closePlaylistsDisplay)
playlistsBlackBoard.addEventListener('click', closePlaylistsDisplay)
createPlaylistBtn.addEventListener('click', showPlaylistForm)
createPlaylistForm.addEventListener('submit', createPlaylist)
impressionBtns.forEach(btn => {
    btn.addEventListener('click', submitImpression)
})

addEventListener('DOMContentLoaded', () => {
    updateImpressionsCount()
})