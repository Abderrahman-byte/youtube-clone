const subscribeBtn = document.getElementById('subscribe-button')

const subscribe = async e => {
    const method = e.target.hasAttribute('data-subscribed') ? 'DELETE': 'POST'
    const channelId = e.target.getAttribute('data-id')

    const req = await fetch('/api/subscribe', {
        'method': method,
        'body': JSON.stringify({'channelId': channelId}),
        'headers': {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })

    console.log(req)
}

if(subscribeBtn !== null) {
    subscribeBtn.addEventListener('click', subscribe)
}