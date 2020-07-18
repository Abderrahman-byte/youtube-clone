const orderBtn = document.getElementById('order-by')
const orderDropDown = document.getElementById('dropdown-list')
const dropDownMenu = document.getElementById('dropdown-menu')
const favBtns = document.querySelectorAll('.videos-container .video .set-favorite')

orderBtn.addEventListener('click', () => {
    orderDropDown.classList.toggle('show')
})

orderDropDown.addEventListener('blur', () => {
    orderDropDown.classList.remove('show')
})

const toggleFav = async (e) => {
    const channelId = e.target.getAttribute('data-channel') || e.target.parentNode.getAttribute('data-channel')
    const videoId = e.target.getAttribute('data-id') || e.target.parentNode.getAttribute('data-id')
    const isFav = e.target.hasAttribute('data-fav') || e.target.parentNode.hasAttribute('data-fav')
    let data = {}

    if(isFav) {
        data = {'channelId': channelId, 'videoId': null}
    } else {
        data = {'channelId': channelId, 'videoId': videoId}
    }

    const req = await fetch('/api/channel', {
        'method': 'PUT',
        'body': JSON.stringify(data),
        'headers': {
            'X-CSRFToken': getCookie('csrftoken')
        },
    })

    if (req.status >= 200 && req.status < 300) {
        favBtns.forEach(btn => {
            btn.classList.remove('favorite')
            btn.removeAttribute('data-fav')
        })

        if(e.target.hasAttribute('data-id') && !isFav) {
            e.target.classList.add('favorite')
            e.target.setAttribute('data-fav', true)
        } else if(!isFav) {
            e.target.parentNode.classList.add('favorite')
            e.target.parentNode.setAttribute('data-fav', true)
        }
    }
    
}

favBtns.forEach(btn => btn.addEventListener('click', toggleFav))