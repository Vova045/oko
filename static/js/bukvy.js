const bukva = document.querySelectorAll('.bukvy_fon')[0];
const krug1 = document.querySelectorAll('.bukvy_main')[0];
const krug2 = document.querySelectorAll('.bukvy_main')[1];
const krug3 = document.querySelectorAll('.bukvy_main')[2];
const krug4 = document.querySelectorAll('.bukvy_main')[3];
const krug5 = document.querySelectorAll('.bukvy_main')[4];
const krug6 = document.querySelectorAll('.bukvy_main')[5];
const krug7 = document.querySelectorAll('.bukvy_main')[6];
const dot1 = document.querySelectorAll('.krug')[0];
const dot2 = document.querySelectorAll('.krug')[1];
const dot3 = document.querySelectorAll('.krug')[2];
const dot4 = document.querySelectorAll('.krug')[3];
const dot5 = document.querySelectorAll('.krug')[4];
const dot6 = document.querySelectorAll('.krug')[5];
const dot7 = document.querySelectorAll('.krug')[6];
dot1.style.background = '#ED1B24';

document.querySelector('#bukvy').addEventListener('click', function () {
    bukva.style.display = 'flex';
})

document.addEventListener('keypress', function (e) {
    if(e.keyCode == 27) bukva.style.display = 'none';
}); 

document.querySelectorAll('.krug')[0].addEventListener('click', function () {
    krug7.style.display = 'none';
    krug6.style.display = 'none';
    krug5.style.display = 'none';
    krug4.style.display = 'none';
    krug3.style.display = 'none';
    krug2.style.display = 'none';
    krug1.style.display = 'flex';
    dot1.style.background = '#ED1B24';
    dot2.style.background = '#C4C4C4';
    dot3.style.background = '#C4C4C4';
    dot4.style.background = '#C4C4C4';
    dot5.style.background = '#C4C4C4';
    dot6.style.background = '#C4C4C4';
    dot7.style.background = '#C4C4C4';
})

document.querySelectorAll('.krug')[1].addEventListener('click', function () {
    krug7.style.display = 'none';
    krug6.style.display = 'none';
    krug5.style.display = 'none';
    krug4.style.display = 'none';
    krug3.style.display = 'none';
    krug1.style.display = 'none';
    krug2.style.display = 'flex';
    dot1.style.background = '#C4C4C4';
    dot2.style.background = '#ED1B24';
    dot3.style.background = '#C4C4C4';
    dot4.style.background = '#C4C4C4';
    dot5.style.background = '#C4C4C4';
    dot6.style.background = '#C4C4C4';
    dot7.style.background = '#C4C4C4';
})

document.querySelectorAll('.krug')[2].addEventListener('click', function () {
    krug7.style.display = 'none';
    krug6.style.display = 'none';
    krug5.style.display = 'none';
    krug4.style.display = 'none';
    krug2.style.display = 'none';
    krug1.style.display = 'none';
    krug3.style.display = 'flex';
    dot1.style.background = '#C4C4C4';
    dot2.style.background = '#C4C4C4';
    dot3.style.background = '#ED1B24';
    dot4.style.background = '#C4C4C4';
    dot5.style.background = '#C4C4C4';
    dot6.style.background = '#C4C4C4';
    dot7.style.background = '#C4C4C4';
})

document.querySelectorAll('.krug')[3].addEventListener('click', function () {
    krug7.style.display = 'none';
    krug6.style.display = 'none';
    krug5.style.display = 'none';
    krug3.style.display = 'none';
    krug2.style.display = 'none';
    krug1.style.display = 'none';
    krug4.style.display = 'flex';
    dot1.style.background = '#C4C4C4';
    dot2.style.background = '#C4C4C4';
    dot3.style.background = '#C4C4C4';
    dot4.style.background = '#ED1B24';
    dot5.style.background = '#C4C4C4';
    dot6.style.background = '#C4C4C4';
    dot7.style.background = '#C4C4C4';
})

document.querySelectorAll('.krug')[4].addEventListener('click', function () {
    krug7.style.display = 'none';
    krug6.style.display = 'none';
    krug4.style.display = 'none';
    krug3.style.display = 'none';
    krug2.style.display = 'none';
    krug1.style.display = 'none';
    krug5.style.display = 'flex';
    dot1.style.background = '#C4C4C4';
    dot2.style.background = '#C4C4C4';
    dot3.style.background = '#C4C4C4';
    dot4.style.background = '#C4C4C4';
    dot5.style.background = '#ED1B24';
    dot6.style.background = '#C4C4C4';
    dot7.style.background = '#C4C4C4';
})
document.querySelectorAll('.krug')[5].addEventListener('click', function () {
    krug7.style.display = 'none';
    krug6.style.display = 'flex';
    krug4.style.display = 'none';
    krug3.style.display = 'none';
    krug2.style.display = 'none';
    krug1.style.display = 'none';
    krug5.style.display = 'none';
    dot1.style.background = '#C4C4C4';
    dot2.style.background = '#C4C4C4';
    dot3.style.background = '#C4C4C4';
    dot4.style.background = '#C4C4C4';
    dot5.style.background = '#C4C4C4';
    dot6.style.background = '#ED1B24';
    dot7.style.background = '#C4C4C4';
})
document.querySelectorAll('.krug')[6].addEventListener('click', function () {
    krug7.style.display = 'flex';
    krug6.style.display = 'none';
    krug4.style.display = 'none';
    krug3.style.display = 'none';
    krug2.style.display = 'none';
    krug1.style.display = 'none';
    krug5.style.display = 'none';
    dot1.style.background = '#C4C4C4';
    dot2.style.background = '#C4C4C4';
    dot3.style.background = '#C4C4C4';
    dot4.style.background = '#C4C4C4';
    dot5.style.background = '#C4C4C4';
    dot6.style.background = '#C4C4C4';
    dot7.style.background = '#ED1B24';
})

document.querySelectorAll('.strelka_slider_right')[0].addEventListener('click', function () {
    if (krug1.style.display === 'flex') {
        krug1.style.display = 'none';
        krug2.style.display = 'flex';
        dot1.style.background = '#C4C4C4';
        dot2.style.background = '#ED1B24';
    }
    else if (krug2.style.display === 'flex') {
        krug2.style.display = 'none';
        krug3.style.display = 'flex';
        dot2.style.background = '#C4C4C4';
        dot3.style.background = '#ED1B24';
    }
    else if (krug3.style.display === 'flex') {
        krug3.style.display = 'none';
        krug4.style.display = 'flex';
        dot3.style.background = '#C4C4C4';
        dot4.style.background = '#ED1B24';
    }
    else if (krug4.style.display === 'flex') {
        krug4.style.display = 'none';
        krug5.style.display = 'flex';
        dot4.style.background = '#C4C4C4';
        dot5.style.background = '#ED1B24';
    }
    else if (krug5.style.display === 'flex') {
        krug5.style.display = 'none';
        krug6.style.display = 'flex';
        dot5.style.background = '#C4C4C4';
        dot6.style.background = '#ED1B24';
    }
    else if (krug6.style.display === 'flex') {
        krug6.style.display = 'none';
        krug7.style.display = 'flex';
        dot6.style.background = '#C4C4C4';
        dot7.style.background = '#ED1B24';
    }
})

document.querySelectorAll('.strelka_slider_left')[0].addEventListener('click', function () {
    if (krug5.style.display === 'flex') {
        krug5.style.display = 'none';
        krug4.style.display = 'flex';
        dot5.style.background = '#C4C4C4';
        dot4.style.background = '#ED1B24';
    }
    else if (krug4.style.display === 'flex') {
        krug4.style.display = 'none';
        krug3.style.display = 'flex';
        dot4.style.background = '#C4C4C4';
        dot3.style.background = '#ED1B24';
    }
    else if (krug3.style.display === 'flex') {
        krug3.style.display = 'none';
        krug2.style.display = 'flex';
        dot3.style.background = '#C4C4C4';
        dot2.style.background = '#ED1B24';
    }
    else if (krug2.style.display === 'flex') {
        krug2.style.display = 'none';
        krug1.style.display = 'flex';
        dot2.style.background = '#C4C4C4';
        dot1.style.background = '#ED1B24';
    }
    else if (krug6.style.display === 'flex') {
        krug6.style.display = 'none';
        krug5.style.display = 'flex';
        dot6.style.background = '#C4C4C4';
        dot5.style.background = '#ED1B24';
    }
    else if (krug7.style.display === 'flex') {
        krug7.style.display = 'none';
        krug6.style.display = 'flex';
        dot7.style.background = '#C4C4C4';
        dot6.style.background = '#ED1B24';
    }
})

document.addEventListener('keypress', function (e) {
    if(e.keyCode == 27) bukva.style.display = 'none';
}); 

document.querySelectorAll('.bukvy_close')[0].addEventListener('click', function () {
    bukva.style.display = 'none';
})