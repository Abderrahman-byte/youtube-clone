const subscribeBtn = document.getElementById('subscribe-button')

const subscribe = async e => {
    const method = e.target.hasAttribute('data-subscribed') ? 'DELETE': 'POST'
    const channelId = e.target.getAttribute('data-id')
    const btnText = method === 'POST' ? 'Subscribed' : 'Subscribe'

    const req = await fetch('/api/subscribe', {
        'method': method,
        'body': JSON.stringify({'channelId': channelId}),
        'headers': {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })

    if (req.status >= 200 && req.status < 300) {
        e.target.toggleAttribute('data-subscribed')
        e.target.textContent = btnText
    } else {
        showAuthDisplay()
    }
}

if(subscribeBtn !== null) {
    subscribeBtn.addEventListener('click', subscribe)
}