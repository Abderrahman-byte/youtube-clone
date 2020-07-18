const backboard = document.getElementById('backboard')
const navCloser = document.getElementById('hide_nav')
const nav = document.getElementById('nav')
const navBars = document.getElementById('nav_bars')
const navPlaylist = document.getElementById('nav_bar_playlists')

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

const renderTextProperly = () => {
    const textBlock = document.querySelectorAll('.text-block')

    textBlock.forEach(blk => {
        const content = blk.textContent.split('\n').join('<br/>')
        blk.innerHTML = content
    })
}

const renderPlaylists = async () => {
    const req = await fetch('/api/playlists', {
        'redirect': 'manual'
    })

    if(req.status >= 200 && req.status < 300) {
        const response = await req.json()
        const playlists = response.playlists
        navPlaylist.innerHTML = ''

        playlists.forEach(pl => {
            const item = document.createElement('li')
            const pLink = document.createElement('a')
            pLink.textContent = pl.title
            pLink.href = `/playlist?id=${pl.id}`
            item.appendChild(pLink)
            navPlaylist.appendChild(item)
        })
    }
}

const hideNav = () => {
    nav.classList.remove('show')
    backboard.style.display = 'none'
}

const showNav = () => {
    nav.classList.add('show')
    backboard.style.display = 'block'
}

navCloser.addEventListener('click', hideNav)
backboard.addEventListener('click', hideNav)
navBars.addEventListener('click', showNav)

addEventListener('DOMContentLoaded', () => {
    renderTextProperly()
    renderPlaylists()
})