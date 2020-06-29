const switcher = document.getElementById('theme_switch')
const root = document.documentElement

const themes = {
    'dark': {
        '--background-a' : '#181818',
        '--background-b' : '#202020',
        '--background-c' : '#121212',
        '--background-d' : '#313131',
        '--variant-clr' : '#ffffff',
        '--icons-clr' : '#909090',
        '--borders-clr': '#303030',
    },
    'light' : {
        '--background-a' : '#F9F9F9',
        '--background-b' : '#FFFFFF',
        '--background-c' : '#FFFFFF',
        '--background-d' : '#F0F0F0',
        '--variant-clr' : '#606060',
        '--icons-clr' : '#606060',
        '--borders-clr': '#d3d3d3',
    }
}

const init = () => {
    const currentTheme = sessionStorage.getItem('theme') || 'light'

    for(const clr in themes[currentTheme]) {
        root.style.setProperty(clr, themes[currentTheme][clr])
    }

    if(currentTheme === 'dark' && !switcher.checked) {
        switcher.click()
    } 
}

const changeTheme = e => {
    const currentTheme = e.target.checked?'dark':'light'
    sessionStorage.setItem('theme', currentTheme)

    for(const clr in themes[currentTheme]) {
        root.style.setProperty(clr, themes[currentTheme][clr])
    }
}

addEventListener('load', init)
switcher.addEventListener('change', changeTheme)