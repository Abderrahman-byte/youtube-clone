const orderBtn = document.getElementById('order-by')
const orderDropDown = document.getElementById('dropdown-list')
const dropDownMenu = document.getElementById('dropdown-menu')

orderBtn.addEventListener('click', () => {
    orderDropDown.classList.toggle('show')
})

orderDropDown.addEventListener('blur', () => {
    orderDropDown.classList.remove('show')
})