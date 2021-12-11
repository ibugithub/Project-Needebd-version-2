
function scrollFunc(elm){
  catName = elm.getAttribute('targetElm')
  const targetElm = document.getElementById(catName)

  console.log(targetElm)
  $('html').animate({scrollTop: targetElm.offsetTop-90});
}
