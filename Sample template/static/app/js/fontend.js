// Site Menu Bar
const navIcon = document.querySelector('.nav_icon')
const siteCloseBtn = document.querySelector('.site-menu-close-btn')
const clickBarSiteMenu = document.querySelector('.click-bar-site-menu')
navIcon.addEventListener('click', function(){
clickBarSiteMenu.classList.add('click-bar-site-menu-active')
})
siteCloseBtn.addEventListener('click',function(){
    clickBarSiteMenu.classList.remove('click-bar-site-menu-active')
})
window.addEventListener('click' , e => e.target == clickBarSiteMenu?clickBarSiteMenu.classList.remove('click-bar-site-menu-active'):false);
// Slider Section
const slides =document.querySelector(".slider").children;
const prev = document.querySelector(".prev");
const next = document. querySelector(".next");
const indicator = document.querySelector(".indicator")
let index =0;
prev.addEventListener("click", function(){
    prevSlide();
    updateCircleIndicator();
    restTimer();
})
next.addEventListener("click", function(){
    nextSlide();
    updateCircleIndicator();
})
function prevSlide(){
    if(index== 0){
        index=slides.length-1;
    }else{
        index--
    }
    changeSlide(  )
}
function nextSlide(){
    if(index== slides.length-1){
        index=0;
    } else{
        index++
    }
   changeSlide()
}
function changeSlide(){
    for(let i= 0; i<slides.length; i++){
        slides[i].classList.remove("active")
    }
    slides[index].classList.add("active");
}
// create indicators
function circleIndicator(){
    for(let i= 0; i< slides.length; i++){
        const div = document.createElement("div");
        div.innerHTML=i+ 1;
        div.setAttribute('onclick', 'indicateSlide(this')
        div.id = i;
        if(i ==0){
            div.className=('active')
        }
        indicator.appendChild(div)
    }
}
circleIndicator()
function updateCircleIndicator(){
    for(let i = 0; i<indicator.children.length; i++){
        indicator.children[i].classList.remove('active');
    }
    indicator.children[index].classList.add('active')
}
function indicateSlide(element){
    index= element.id;
    changeSlide();
    updateCircleIndicator();
}
// Auto play
function restTimer(){
    clearInterval(timer)
    timer = setInterval(autoPlay,6000)
}
function autoPlay(){
    nextSlide()
    updateCircleIndicator()
}
let timer =setInterval(autoPlay,6000);
// Slider Section End
//Account Bar 
const accountButton = document.querySelector('.account-subcontainer')
const accountCloseButton = document.querySelector('.close-account-btn')
const accountDropDown = document.querySelector('.account-dropdown-main')
accountButton.addEventListener('click', function(){
    accountDropDown.classList.add('account-dropdown-main-active')
})
accountCloseButton.addEventListener('click', function(){
    accountDropDown.classList.remove('account-dropdown-main-active')
})
window.addEventListener('click', e => e.target ==accountDropDown ? accountDropDown.classList.remove('account-dropdown-main-active'):true)

// countdown section
function getTimeRemaining(endtime) {
    var t = Date.parse(endtime) - Date.parse(new Date());
    var seconds = Math.floor((t / 1000) % 60);
    var minutes = Math.floor((t / 1000 / 60) % 60);
    var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
    var days = Math.floor(t / (1000 * 60 * 60 * 24));
    return {
      'total': t,
      'days': days,
      'hours': hours,
      'minutes': minutes,
      'seconds': seconds
    };
  }
  function initializeClock(id, endtime) {
    var clock = document.getElementById(id);
    var daysSpan = clock.querySelector('.days');
    var hoursSpan = clock.querySelector('.hours');
    var minutesSpan = clock.querySelector('.minutes');
    var secondsSpan = clock.querySelector('.seconds');
    function updateClock() {
      var t = getTimeRemaining(endtime);
      daysSpan.innerHTML = ("0")+ t.days + (' :');
      hoursSpan.innerHTML = ('' + t.hours) +(' :').slice(-2);
      minutesSpan.innerHTML = (''+t.minutes)+(' :').slice(-2);
      secondsSpan.innerHTML = ('' + t.seconds ).slice(-2);
      if (t.total <= 0) {
        clearInterval(timeinterval);
      }
    }
    updateClock();
    var timeinterval = setInterval(updateClock, 1000);
  }
  var deadline = new Date(Date.parse(new Date()) + 2 * 24 * 60 * 60 * 1000);
  initializeClock('clockdiv', deadline);
