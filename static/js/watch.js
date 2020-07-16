const video_ = document.getElementById('video')
const impressionBtns = [document.getElementById('like-btn'), document.getElementById('dislike-btn')]
const impressionCounts = [document.getElementById('likes-count'), document.getElementById('dislikes-count')]
const subscount = document.getElementById('subs-count')
const saveBtn = document.getElementById('save-playlist')
const playlistsBlackBoard = document.getElementById('playlists-blackboard')
const playlistsDisplay = document.getElementById('playlists-container')
const playlistContainer = document.getElementById('playlists')
const closePlaylistsBtn = document.getElementById('close-playlists')
const createPlaylistBtn = document.getElementById('create-playlist')
const createPlaylistForm = document.getElementById('playlist-form')
const playlistFormError = document.querySelector('.playlist-form .error')
const authDisplay = document.getElementById('auth-display')
const authBackboard = document.getElementById('auth-blackboard')
const closeAuthDisplayBtn = document.getElementById('close-auth')
const descritpionDiv = document.getElementById('video-description')
const toggleDescriptionBtn = document.getElementById('show-decription-btn')
const togglePlaylistBtn = document.getElementById('toggle-playlist')
const playlistElt = document.querySelector('.playlist')

////////////////////// Show and Close Displays //////////////////////

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

const closeAuthDisplay = () => {
    authDisplay.style.display = 'none'
    authBackboard.style.display =  'none'
}

const showAuthDisplay = () => {
    authDisplay.style.display = 'flex'
    authBackboard.style.display =  'block'
}

const toggleDescription = () => {
    descritpionDiv.classList.toggle('show')
}

const togglePlaylist = () => {
    if(playlistElt) {
        playlistElt.classList.toggle('hide')
    }
}

////////////////////// Utilities functions //////////////////////

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

const updateSuscriptionsCount = () => {
    const count = parseInt(subscount.getAttribute('data-count'), 10) || 0
    subscount.textContent = formatCount(count)
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

const updateViews = () => {
    const views = document.querySelectorAll('.related .video .views')
    views.forEach(viewSpan => {
        const viewsCount = Number(viewSpan.getAttribute('data-views')) || 0
        viewSpan.textContent = formatCount(viewsCount)
    })
}

const renderDescription = () => {
    if (descritpionDiv !== null ) {
        const decsriptionHtml = descritpionDiv.textContent.split('\n').join('<br/>')
        descritpionDiv.innerHTML = decsriptionHtml       
    }
}

const fixPlaylistHeight = () => {
    const plHeader = document.querySelector('.playlist .header')
    const plBody = document.querySelector('.playlist .body')

    if(plHeader && plBody) {
        const headerHeigth = parseFloat(getComputedStyle(plHeader).height)
        const videoHeigth = parseFloat(getComputedStyle(video_).height)

        plBody.style.height = (videoHeigth - headerHeigth) + 'px'
    }
}

////////////////////// HTTP Requests and ajax functions //////////////////////

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
            },
        })

        if(req.redirected && (req.url.indexOf('login') >= 0 || req.url.indexOf('register') >= 0)) {
            showAuthDisplay()
        } else if (req.status >= 200 && req.status < 300) {
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
    const playlistElt = document.querySelector('.playlist')

    const data = {'videoId': videoId, 'playlistId': playlistId, 'action': action}
    const req = await fetch('/api/playlists', {
        'method': 'PUT',
        'body': JSON.stringify(data),
        'headers': {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })

    if(playlistElt && 
        req.status >= 200 && 
        req.status < 300 && 
        action === -1 && 
        playlistId == playlistElt.getAttribute('data-id')) {
        playlistElt.parentNode.removeChild(playlistElt)
    }
}

const saveVideo = async () => {
    const req = await fetch('/api/playlists')

    if(req.redirected && (req.url.indexOf('login') >= 0 || req.url.indexOf('register') >= 0)) {
        showAuthDisplay()
    } else if (req.status >= 200 && req.status < 300) {
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

const createPlaylist = async e => {
    e.preventDefault()
    const title = e.target.title.value
    const privacy = e.target.privacy.checked
    const videoId = video_.getAttribute('data-id')
    const data = {title, privacy, videoId}

    const req = await fetch('/api/playlists', {
        'method': 'POST',
        'body': JSON.stringify(data),
        'headers' : {
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

const submitView =  e => {
    const time = video_.currentTime
    const id = e.target.getAttribute('data-id')

    if(time >= 6 ) {
        fetch('/api/submitview', {
            'method': 'POST',
            'body': JSON.stringify({'id': id}),
            'headers' : {
                'X-CSRFToken': getCookie('csrftoken') 
            }
        })

        e.target.removeEventListener('timeupdate', submitView)
    }

}

////////////////////// Events listeners //////////////////////

saveBtn.addEventListener('click', saveVideo)
closePlaylistsBtn.addEventListener('click', closePlaylistsDisplay)
playlistsBlackBoard.addEventListener('click', closePlaylistsDisplay)
createPlaylistBtn.addEventListener('click', showPlaylistForm)
createPlaylistForm.addEventListener('submit', createPlaylist)
closeAuthDisplayBtn.addEventListener('click', closeAuthDisplay)
authBackboard.addEventListener('click', closeAuthDisplay)
video_.addEventListener('timeupdate', submitView)

if(toggleDescriptionBtn !== null ){
    toggleDescriptionBtn.addEventListener('click', e => {
        toggleDescription()
        const btnText = descritpionDiv.classList.contains('show') ? 'Less' :'More'
        e.target.textContent = btnText
    })
}


impressionBtns.forEach(btn => {
    btn.addEventListener('click', submitImpression)
})

addEventListener('DOMContentLoaded', () => {
    updateImpressionsCount()
    updateSuscriptionsCount()
    renderDescription()
    updateViews()

    if(togglePlaylistBtn) {
        togglePlaylistBtn.addEventListener('click', togglePlaylist)
    }
})

video_.addEventListener('loadedmetadata', () => {
    fixPlaylistHeight()
})