const video = document.getElementById('video')
const videoContainer = document.getElementById('video-container')
const videoControls = document.getElementById('video_controls')
const playBtn = document.getElementById('play')
const volumeBtn = document.getElementById('volume-button')
const volumeRange = document.getElementById('volume')
const progressBar = document.getElementById('progress-bar')
const seek = document.getElementById('seek')
const timeEllapse = document.getElementById('time-ellapse')
const durationData = document.getElementById('duration')
const seekTooltip = document.getElementById('seek-tooltip')
const fullScreenBtn = document.getElementById('fullscreen-button')
const pipBtn = document.getElementById('pip-button')

const formatTime = time => {
    let hours = Math.floor(time / 3600)
    let minutes = Math.floor((time - (hours * 3600)) / 60)
    let secondes = Math.floor(time - (hours * 3600) - (minutes * 60))
    
    if(hours < 10) {
        hours = '0' + hours
    }

    if(minutes < 10) {
        minutes = '0' + minutes
    }

    if(secondes < 10) {
        secondes = '0' + secondes
    }

    return Number(hours) > 0 ? `${hours}:${minutes}:${secondes}`:`${minutes}:${secondes}`
} 

const initializeVideo = () => {
    const duration = Math.round(video.duration)
    progressBar.setAttribute('max', duration)
    seek.setAttribute('max', duration)
    durationData.textContent = formatTime(duration)
}

const hideControls = () => {
    if(!video.paused) {
        videoControls.classList.add('hide')
    }
}

const showControls = () => {
    videoControls.classList.remove('hide')
}

const togglePip = async () => {
    if(document.pictureInPictureElement) {
        await document.exitPictureInPicture()
    } else {
        await video.requestPictureInPicture()
    }
}

// Play controls
const setUpPlayPauseIcons = () => {
    const icons = playBtn.querySelectorAll('use')
    if(video.paused || video.ended) {
        icons[1].classList.add('hidden')
        icons[0].classList.remove('hidden')
        playBtn.setAttribute('data-title', 'Play (k)')
    } else {
        icons[0].classList.add('hidden')
        icons[1].classList.remove('hidden')
        playBtn.setAttribute('data-title', 'Pause (k)')
    }
}

const togglePlay = () => {
    if(video.paused || video.ended) {
        video.play()
    } else {
        video.pause()
    }
    setUpPlayPauseIcons()
}

// Volume control
const updateVolumeIcon = () => {
    const icons = volumeBtn.querySelectorAll('use')
    if(video.muted || video.volume <= 0.01) {
        icons[2].classList.add('hidden')
        icons[1].classList.add('hidden')
        icons[0].classList.remove('hidden')
        volumeBtn.setAttribute('data-title', 'Unmute (m)')
    } else if(video.volume <= 0.5) {
        icons[0].classList.add('hidden')
        icons[2].classList.add('hidden')
        icons[1].classList.remove('hidden')
        volumeBtn.setAttribute('data-title', 'Mute (m)')
    } else {
        icons[0].classList.add('hidden')
        icons[1].classList.add('hidden')
        icons[2].classList.remove('hidden')
        volumeBtn.setAttribute('data-title', 'Mute (m)')
    }
}

const toggleVolume = () => {
    video.muted = !video.muted
    if(video.muted) {
        volumeRange.value = 0
    } else {
        volumeRange.value = video.volume
    }
    updateVolumeIcon()
}

const setVolume = e => {
    const v = e.target.value
    if(v <= 0) {
        video.muted = true
    } else {
        video.muted = false
        video.volume = v
    }

    updateVolumeIcon()
}

const volumeUp = () => {
    if(video.volume < 1) {
        video.volume += 0.1
    } else {
        video.volume = 1
    }
    volumeRange.value = video.volume
    updateVolumeIcon()
}

const volumeDown = () => {
    if(video.volume > 0) {
        video.volume -= 0.1
    } else {
        video.volume = 0
    }
    volumeRange.value = video.volume
    updateVolumeIcon()
}

// Progress Control
const updateEllapse = () => {
    const time = formatTime(video.currentTime)
    timeEllapse.textContent = time
}

const setProgress = () => {
    seek.value = Math.floor(video.currentTime);
    progressBar.value = Math.floor(video.currentTime);
    updateEllapse()
}

const updateSeekTooltip = e => {
    const skipTo = Math.round(e.offsetX / e.target.clientWidth * parseInt(e.target.getAttribute('max', 10)))
    seek.setAttribute('data-seek', skipTo)
    const time = formatTime(skipTo)
    seekTooltip.textContent = time
    const rect = video.getBoundingClientRect();
    seekTooltip.style.left = `${event.pageX - rect.left}px`;
}

const updateProgress = e => {
    const skipTo = event.target.dataset.seek
    ? event.target.dataset.seek
    : event.target.value;
    video.currentTime = parseInt(skipTo)
    progressBar.value = skipTo
    seek.value = skipTo
    console.log(skipTo)
}

// Full screen control
const updateFullscreenIcons = () => {
    const icons = fullScreenBtn.querySelectorAll('use')
    if(document.fullscreen) {
        icons[1].classList.remove('hidden')
        icons[0].classList.add('hidden')
    } else {
        icons[1].classList.add('hidden')
        icons[0].classList.remove('hidden')
    }
}

const toggleFullscreen = async () => {
    if(document.fullscreen) {
        await document.exitFullscreen()
    } else {
        await videoContainer.requestFullscreen()
    }
    updateFullscreenIcons()
}

// short cuts control
const shortCuts = e => {
    const key = e.keyCode
    
    switch(key) {
        case 75 :
        case 32 :
            togglePlay()
            break
        
        case 77 :
            toggleVolume()
            break

        case 70 :
            toggleFullscreen()
            break

        case 40 :
            volumeDown()
            break

        case 38:
            volumeUp()
            break

        case 37 :
            video.currentTime -= 5
            break
        
        case 39:
            video.currentTime += 5
            break

        case 80 :
            togglePip()
            break
    }
}

const disableShortCuts = () => {
    document.removeEventListener('keyup', shortCuts)
}

const enableShortCuts = () => {
    document.addEventListener('keyup', shortCuts)
}

// Events  
playBtn.addEventListener('click', togglePlay)
video.addEventListener('click', togglePlay)
video.addEventListener('timeupdate', setProgress)
video.addEventListener('ended', setUpPlayPauseIcons)
seek.addEventListener('mousemove', updateSeekTooltip)
seek.addEventListener('input', updateProgress)
volumeBtn.addEventListener('click', toggleVolume)
volumeRange.addEventListener('input', setVolume)
fullScreenBtn.addEventListener('click', toggleFullscreen)
pipBtn.addEventListener('click', togglePip)
videoContainer.addEventListener('mouseleave', hideControls)
videoContainer.addEventListener('mouseenter', showControls)

document.addEventListener('keyup', shortCuts)
document.addEventListener('DOMContentLoaded', () => {
    const src = video.currentSrc
    video.setAttribute('src', src)
    video.addEventListener('loadedmetadata', initializeVideo)
})

document.querySelectorAll('input, texterea').forEach(elt => {
    elt.addEventListener('focus', disableShortCuts)
    elt.addEventListener('blur', enableShortCuts)
})