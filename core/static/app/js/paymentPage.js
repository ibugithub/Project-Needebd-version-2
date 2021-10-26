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



// making the choice function to select only one choice......
var PTPayButton = document.getElementById('PTPayBtn');
var cODElement = document.getElementById('cODCheckbox');
var selectionError = document.getElementById('selectionError');
var curierSelectionError = document.getElementById('curierSelectionError');

// Remove all the prvious checked selection ...
var curierSelector = document.getElementsByClassName("curier");
function previousCheckedRemoved(){
  let len = curierSelector.length;
  for (let i = 0; i < len; i++){
    curierSelector[i].checked = false
  }
}

// will checked the current clicked icon ...
let len2 = curierSelector.length
for (let i = 0; i < len2; i++){
  curierSelector[i].addEventListener('click', function(){
    previousCheckedRemoved()
    console.log("all previous checked item unchecked")
    curierSelector[i].checked = true
    curierSelectionError.innerHTML = ""
    PTPayButton.removeAttribute("disabled")
  })
}

// Will get The value of checked icon ...
function curierValueGetter(){
  let len = curierSelector.length 
  for (let i = 0; i < len; i++){
    if(curierSelector[i].checked){
      return curierSelector[i].value
    }
  }
}


//function for Making Procced To Pay button disabled if not select any option ....
PTPayButton.addEventListener('mouseover', function(){
  if (cODElement.checked == false)
  {
    selectionError.innerHTML = "You must select an option"
    PTPayButton.setAttribute('disabled', "disabled")
  }
  if(curierValueGetter() == undefined){
    curierSelectionError.innerHTML = "you must select a curier service"
    PTPayButton.setAttribute("disabled", "disabled")
  }
})

// will remove the selection error when cash on delivery checkbox will be checked
cODElement.addEventListener('change', function(){
  if (cODElement.checked)
  { PTPayButton.removeAttribute('disabled')
    document.getElementById('selectionError').innerHTML = ""
  }
})





