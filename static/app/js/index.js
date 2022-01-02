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




// Scrolling the sliding item section1
  var rightArrow1 = document.getElementById('rightArrow1');
  var leftArrow1 = document.getElementById('leftArrow1');
  var content = document.getElementById('movingContent');
  var position = 0;
  var innerContent = document.getElementsByClassName('innerContent');
  var icontainer = document.getElementById("iContainer")
  var totalContentLength = 0
  leftArrow1.addEventListener('click', function () {
    if (position != 0) {
      let margin = 400
      position += margin
      let value = position + "px"
      content.style.marginLeft = value
      content.style.transition = "all .2s"
    }
  })
  rightArrow1.addEventListener('click', function () {
    let len = innerContent.length;
    var totalContentLength = 0;
    for (let i = 0; i < len; i++) {
      var cLength = innerContent[i].clientWidth;
      totalContentLength += cLength + 13
    }
    totalContentLength -= iContainer.clientWidth
    if (position > -totalContentLength) {
      let margin = -400
      position += margin
      let value = position + "px"
      content.style.marginLeft = value
      content.style.transition = "all .2s"
    } 
    // for removing the extra white space after getting margin..
    if (position < -totalContentLength) {
      let diff = position + totalContentLength
      let val = position - diff
      content.style.marginLeft = val + "px"
      content.style.transition = "all .2s"
    }
  })


// Scrolling the sliding item section2
  var rightArrow2 = document.getElementById('rightArrow2');
  var leftArrow2 = document.getElementById('leftArrow2');
  var content2 = document.getElementById('movingContent2');
  var position2 = 0;
  var innerContent2 = document.getElementsByClassName('innerContent2');
  var icontainer2 = document.getElementById("iContainer2")
  var totalContentLength2 = 0
  leftArrow2.addEventListener('click', function () {
    if (position2 != 0) {
      let margin = 400
      position2 += margin
      let value = position2 + "px"
      content2.style.marginLeft = value
      content2.style.transition = "all .2s"
    }
  })
  rightArrow2.addEventListener('click', function () {
    let len2 = innerContent2.length;
    var totalContentLength2 = 0;
    for (let i = 0; i < len2; i++) {
      var cLength2 = innerContent2[i].clientWidth;
      totalContentLength2 += cLength2 + 13
    }
    totalContentLength2 -= iContainer2.clientWidth
    if (position2 > -totalContentLength2) {
      let margin = -400
      position2 += margin
      let value = position2 + "px"
      content2.style.marginLeft = value
      content2.style.transition = "all .2s"
    }
    if (position2 < -totalContentLength2) {
      let diff = position2 + totalContentLength2
      let val = position2 - diff
      content2.style.marginLeft = val + "px"
      content2.style.transition = "all .2s"
    }
  })
