'use strict';

$(function(){
  $('.slider').bxSlider({
    mode: 'fade',
    captions: true,
    slideWidth: 1600,
  });
});
// ハンバーガーメニュー
  const open = document.getElementById('open');
  const overlay = document.querySelector('.overlay');
  const close= document.getElementById('close');
  
  open.addEventListener('click',() =>{
    overlay.classList.add('show');
    open.classList.add('hide');
  });
  close.addEventListener('click',() =>{
    overlay.classList.remove('show');
    open.classList.remove('hide');
  });

