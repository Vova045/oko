const krug1 = document.querySelectorAll('.bukvy_main')[0];
const krug2 = document.querySelectorAll('.bukvy_main')[1];
const krug3 = document.querySelectorAll('.bukvy_main')[2];
const krug4 = document.querySelectorAll('.bukvy_main')[3];
const krug5 = document.querySelectorAll('.bukvy_main')[4];
const krug6 = document.querySelectorAll('.bukvy_main')[5];
const krug7 = document.querySelectorAll('.bukvy_main')[6];


document.querySelectorAll('.strelka_slider_right')[0].addEventListener('click', function () {
    if (krug1.style.display === 'flex') {
        krug1.style.display = 'none';
        krug2.style.display = 'flex';
    }
    else if (krug2.style.display === 'flex') {
        krug2.style.display = 'none';
        krug3.style.display = 'flex';
    }
    else if (krug3.style.display === 'flex') {
        krug3.style.display = 'none';
        krug4.style.display = 'flex';
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
    }
    else if (krug6.style.display === 'flex') {
        krug6.style.display = 'none';
        krug7.style.display = 'flex';
    }
})

document.querySelectorAll('.strelka_slider_left')[0].addEventListener('click', function () {
    if (krug5.style.display === 'flex') {
        krug5.style.display = 'none';
        krug4.style.display = 'flex';
    }
    else if (krug4.style.display === 'flex') {
        krug4.style.display = 'none';
        krug3.style.display = 'flex';
    }
    else if (krug3.style.display === 'flex') {
        krug3.style.display = 'none';
        krug2.style.display = 'flex';
    }
    else if (krug2.style.display === 'flex') {
        krug2.style.display = 'none';
        krug1.style.display = 'flex';
    }
    else if (krug6.style.display === 'flex') {
        krug6.style.display = 'none';
        krug5.style.display = 'flex';
    }
    else if (krug7.style.display === 'flex') {
        krug7.style.display = 'none';
        krug6.style.display = 'flex';
    }
})