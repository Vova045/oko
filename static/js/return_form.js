
// Появление заявки на обратную связь
const div = document.querySelectorAll('.bg-modal')[0];

document.querySelectorAll('.zayavka')[0].addEventListener('click', function () {
    div.style.display = 'flex';
})

// document.querySelectorAll('.topcontent_zayavka')[0].addEventListener('click', function () {
//     div.style.display = 'flex';
// })


document.addEventListener('keypress', function (e) {
    if(e.keyCode == 27) div.style.display = 'none';
}); 

document.querySelectorAll('.modal-close')[0].addEventListener('click', function () {
    div.style.display = 'none';
})

// Закрытие сообщения, что письмо отправлено
var selection = document.querySelectorAll('.mail_sent-close')[0] !== undefined;
if (selection) {
    document.querySelectorAll('.mail_sent-close')[0].addEventListener('click', function () {
        document.querySelectorAll('.bg-modal_sent')[0].style.display = 'none';
    })
}
