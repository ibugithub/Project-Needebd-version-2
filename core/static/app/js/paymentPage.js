function payment(evt, paymentName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(paymentName).style.display = "block";
    evt.currentTarget.className += " active";
  }
document.getElementById("defaultOpen").click();


button = document.getElementById('PTPayBtn')
document.getElementsByClassName('cash-on-delivery')[0].addEventListener('click', function(e){
  if (e.currentTarget.classList.contains('border'))
  {
    e.currentTarget.classList.remove('border')
    document.getElementById('paymentMethodWarning'). innerHTML = "select one payment method option"
  }
  else{
    e.currentTarget.classList.add('border')
    document.getElementById('paymentMethodWarning'). innerHTML = ""
    button.disabled = false
    button.style.cursor = "pointer"
  }
})


// This section is for courier selection
courier = document.getElementsByClassName('courier-name')
let len3 = courier.length
for (let  i = 0; i < len3; i++){
  courier[i].addEventListener('click', function(){
    if (courier[i].classList.contains('border')){
      document.getElementById('courierWarning').innerHTML = "select one courier option"
      courier[i].classList.remove('border');
    }
    else{
      prevClassRemover()
      courier[i].classList.add('border');
      document.getElementById('courierWarning').innerHTML = ""
    }
  })
}
function prevClassRemover(){
  for (let i = 0; i < len3; i++){
    
    if(courier[i].classList.contains('border')){
      courier[i].classList.remove('border')
    }
    
  }
}
function courierSelectionChecker(){
  for (let i = 0; i < len3; i++){
    if(courier[i].classList.contains('border')){
      return true
    }
  }
}


// This section is for managing the Procced to button whether to clickable or not
button.addEventListener("mouseover", buttonManager);
function buttonManager(){
  currentTab = document.getElementsByClassName('active')[0].getAttribute('value')
  if (currentTab == "D/CCard"){
    console.log("This is 1")
  }
  if (currentTab == "Net Banking"){
    console.log("This is 2")
  } 
  if (currentTab == "cashOn"){
    if (document.getElementsByClassName('cash-on-delivery')[0].classList.contains('border'))
    {
      paymentMethod = true
    }
    else{
      paymentMethod = false
    }
  }

  if (paymentMethod == false){
    document.getElementById('paymentMethodWarning').innerHTML = "select one payment method option"
    button.disabled = true
    button.style.cursor = "not-allowed"
  }
 
  if (courierSelectionChecker() != true){
    document.getElementById('courierWarning').innerHTML = "select one courier option"
    button.disabled = true
    button.style.cursor = "not-allowed"
  }  
}



// // making the choice function to select only one choice......
// var PTPayButton = document.getElementById('PTPayBtn');
// var cODElement = document.getElementById('cODCheckbox');
// var selectionError = document.getElementById('selectionError');
// var curierSelectionError = document.getElementById('curierSelectionError');

// // Remove all the prvious checked selection ...
// var curierSelector = document.getElementsByClassName("curier");
// function previousCheckedRemoved(){
//   let len = curierSelector.length;
//   for (let i = 0; i < len; i++){
//     curierSelector[i].checked = false
//   }
// }

// // will checked the current clicked icon ...
// let len2 = curierSelector.length
// for (let i = 0; i < len2; i++){
//   curierSelector[i].addEventListener('click', function(){
//     previousCheckedRemoved()
//     console.log("all previous checked item unchecked")
//     curierSelector[i].checked = true
//     curierSelectionError.innerHTML = ""
//     PTPayButton.removeAttribute("disabled")
//     PTPayButton.style.cursor = "pointer"
//   })
// }

// // Will get The value of checked icon ...
// function curierValueGetter(){
//   let len = curierSelector.length 
//   for (let i = 0; i < len; i++){
//     if(curierSelector[i].checked){
//       return curierSelector[i].value
//     }
//   }
// }


// //function for Making Procced To Pay button disabled if not select any option ....
// PTPayButton.addEventListener('mouseover', function(){
//   if (cODElement.checked == false)
//   {
//     selectionError.innerHTML = "You must select an option"
//     PTPayButton.setAttribute('disabled', "disabled")
//     PTPayButton.style.cursor = "not-allowed"
//   }
//   if(curierValueGetter() == undefined){
//     curierSelectionError.innerHTML = "you must select a curier service"
//     PTPayButton.style.cursor = "not-allowed"
//     PTPayButton.setAttribute("disabled", "disabled")
//   }
// })

// // will remove the selection error when cash on delivery checkbox will be checked
// cODElement.addEventListener('change', function(){
//   if (cODElement.checked)
//   { PTPayButton.style.cursor = 'pointer'
//     PTPayButton.removeAttribute('disabled')
//     document.getElementById('selectionError').innerHTML = ""
//   }
// })





