const commentField = document.querySelector('.comment-form .content')
const addCommentBtn = document.querySelector('.comment-form button')
const commentForm = document.querySelector('.comment-form')
const commentsContainer = document.getElementById('comments-list')
const deleteBtns = document.querySelectorAll('.delete-comment')
const commentsCount = document.getElementById('comments-count')
const editBtns = document.querySelectorAll('.edit-comment')

const checkAuth = (e) => {
    disableShortCuts()
    if(e.target.hasAttribute('data-user')) {
        addCommentBtn.style.display = 'block'
    } else {
        showAuthDisplay()
    }
}

const displayCommentsProperly = () => {
    const comments = document.querySelectorAll('.comment .content')
    comments.forEach(c => {
        const content = c.textContent
        c.innerHTML = content.split('\n').join('<br/>')
    })
}

const replaceAllForms = () => {
    const formsComments = document.querySelectorAll('.comment .content-form')
    formsComments.forEach(form => {
        const content = form.getAttribute('data-content')
        const contentElt = document.createElement('p')
        contentElt.innerHTML = content.split('\n').join('<br/>')
        contentElt.setAttribute('data-content', content)
        contentElt.classList.add('content')
        form.parentNode.replaceChild(contentElt, form)
    })
}

const putComment = async (e) => {
    e.preventDefault()
    const id = e.target.getAttribute('data-id')
    const content = e.target.content.value

    if(content !== '') {
        const req = await fetch('/api/comment', {
            'method': 'PUT',
            'body': JSON.stringify({id, content}),
            'headers' : {
                'X-CSRFToken': getCookie('csrftoken') 
            }
        })

        if(req.status >= 200 && req.status < 300) {
            const contentElt = document.createElement('p')
            contentElt.innerHTML = content.split('\n').join('<br/>')
            contentElt.setAttribute('data-content', content)
            contentElt.classList.add('content')
            e.target.parentNode.replaceChild(contentElt, e.target)
        }
    }
}

const deleteComment = async (e) => {
    const id = e.target.getAttribute('data-id') || e.target.parentNode.getAttribute('data-id')
    const req = await fetch('/api/comment', {
        'method': 'DELETE',
        'body': JSON.stringify({id}),
        'headers' : {
            'X-CSRFToken': getCookie('csrftoken') 
        }
    })

    if(req.status >= 200 && req.status < 300) {
        const commentElt = document.getElementById(id)
        commentElt.parentNode.removeChild(commentElt)
        commentsCount.textContent = Number(commentsCount.textContent) - 1
    }
}

const editComment = (e) => {
    replaceAllForms()
    const id = e.target.getAttribute('data-id') || e.target.parentNode.getAttribute('data-id')
    const commentElt = document.getElementById(id)
    const contentElt = commentElt.querySelector('.body .content')
    const currentContent = contentElt.getAttribute('data-content')
    
    const editForm = document.createElement('form')
    editForm.setAttribute('data-id', id)
    editForm.setAttribute('data-content', currentContent)
    editForm.classList.add('content-form')
    editForm.addEventListener('submit', putComment)
    const editField = document.createElement('textarea')
    editField.name = 'content'
    editField.textContent = currentContent
    editField.addEventListener('focus', disableShortCuts)
    editField.addEventListener('blur', enableShortCuts)
    const saveBtn = document.createElement('button')
    saveBtn.textContent = 'save'
    editForm.appendChild(editField)
    editForm.appendChild(saveBtn)

    contentElt.parentNode.replaceChild(editForm, contentElt)
}

const renderComment = (response) => {
    const { id, content, user, profil } = response
    const html = `<div class="comment" id="${id}">
        <a href="/user">
            <img src="${profil}"/>
        </a>
        <div class="body">
            <p class="header"><a href="/user" class="channel-title">${user}</a>
                <span class="date">Just Now</span></p>
            <p class="content" data-content="${content}">${content.split('\n').join('<br/>')}</p>
        </div>
        <div class="control">
            <button data-id="${id}" class="edit-comment"><i class="fas fa-pen"></i></button>
            <button data-id="${id}" class="delete-comment"><i class="fas fa-trash-alt"></i></button>
        </div>
    </div>`
    commentsContainer.innerHTML = html + commentsContainer.innerHTML
    commentsCount.textContent = Number(commentsCount.textContent) + 1
    document.querySelectorAll('.delete-comment').forEach(btn => btn.addEventListener('click', deleteComment))
    document.querySelectorAll('.edit-comment').forEach(btn => btn.addEventListener('click', editComment))
    commentForm.reset()
}

const sendComment = async (id, content) => {
    const data = {id, content}
    const req = await fetch('/api/comment', {
        'method': 'POST',
        'body': JSON.stringify(data),
        'headers' : {
            'X-CSRFToken': getCookie('csrftoken') 
        }
    })

    if(req.status >= 200 && req.status < 300 ) {
        const response = await req.json()
        renderComment(response)
    }
}

const addComment = (e) => {
    e.preventDefault()
    const id = video.getAttribute('data-id')
    const content = e.target.content.value

    if(content !== '') {
        sendComment(id, content)
    }
}

commentField.addEventListener('focus', checkAuth)
commentField.addEventListener('blur', enableShortCuts)
commentForm.addEventListener('submit', addComment)
deleteBtns.forEach(btn => btn.addEventListener('click', deleteComment))
editBtns.forEach(btn => btn.addEventListener('click', editComment))
addEventListener('DOMContentLoaded', () => {
    displayCommentsProperly()
})