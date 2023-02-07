document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('addList').addEventListener('click', (ev) => {
        document.getElementById('newList').style.display= 'flex'
    })
    document.getElementById('cancel').addEventListener('click',()=>{
        document.getElementById('newList').style.display= 'none'
    })
})