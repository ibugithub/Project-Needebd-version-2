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



//function for Making Procced To Pay button disabled if not select any option ....
var PTPayButton = document.getElementById('PTPayBtn')
var cODElement = document.getElementById('cODCheckbox')
PTPayButton.addEventListener('mouseover', function(){
  if (cODElement.checked)
  {console.log("now you will be redirected to the next page")}
  else {
    console.log("you must select one option above")
    let selectionError = document.getElementById('selectionError')
    selectionError.innerHTML = "You must select an option"
    PTPayButton.setAttribute('disabled', "disabled")
  }
})
cODElement.addEventListener('change', function(){
  if (cODElement.checked)
  { PTPayButton.removeAttribute('disabled')
    document.getElementById('selectionError').innerHTML = ""
  }
})


// making the choice function to select only one choice......
var curierSelector = document.getElementsByClassName("curier")
let len = curierSelector.length
for (i = 0; i < len; i++){
  if(curierSelector[i].checked == true){
    console.log("at least one has been selected")
  }
  
}