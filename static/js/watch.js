const video_ = document.getElementById('video')
const impressionBtns = [document.getElementById('like-btn'), document.getElementById('dislike-btn')]
const impressionCounts = [document.getElementById('likes-count'), document.getElementById('dislikes-count')]

const formatCount = count => {
    if(count < 0) {
        return 0
    }

    const md = Math.floor(count / 1000000000)
    const m = Math.floor((count - (md * 1000000000)) / 1000000)
    const k = Math.floor((count - (md * 1000000000) - (m * 1000000)) / 1000) 
    const u = Math.floor(count - (md * 1000000000)  - (m * 1000000) - (m * 1000))
    
    if(md > 0) {
        return `${md}Md`
    } else if (m > 0) {
        return `${m}M`
    } else if(k > 0) {
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
    const method = target.classList.contains('active') ? 'DELETE': 'POST'
    const action = target.getAttribute('data-action') || '1'
    const id = video_.getAttribute('data-id')

    if(method === 'POST') {
        const data = {'id': id, 'kind': action}
        const req = await fetch('/api/impression', {
            'method': 'POST',
            'body': JSON.stringify(data),
            'headers': {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })

        if(req.status >= 200 && req.status < 300) {
            impressionBtns.forEach(btn => {
                if(btn.classList.contains('active')) {
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
    } else if(method === 'DELETE') {
        const data = {'id': id}
        const req = await fetch('/api/impression', {
            'method': 'DELETE',
            'body': JSON.stringify(data),
            'headers': {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })

        if(req.status >= 200 && req.status < 300) {
            const sib = target.nextElementSibling
            const count = parseInt(sib.getAttribute('data-count'), 10) || 0
            sib.setAttribute('data-count', count - 1)
            updateImpressionsCount()
            console.log(count)
            impressionBtns.forEach(btn => btn.classList.remove('active'))
        }
    }
}

impressionBtns.forEach(btn => {
    btn.addEventListener('click', submitImpression)
})

addEventListener('DOMContentLoaded', () => {
    updateImpressionsCount()
})