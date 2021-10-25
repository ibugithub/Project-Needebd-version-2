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

var PTPayButton = document.getElementById('PTPayBtn')

var cODElement = document.getElementById('cODCheckbox')

PTPayButton.addEventListener('mouseover', function(){
  if (cODElement.checked)
  {console.log("now you will be redirected to the next page")}
  else {
    console.log("you must select one option above")
    let selectionError = document.getElementById('selectionError')
    selectionError.innerHTML = "You must select an option"

  }
})

PTPayButton.addEventListener('mouseout', function(){
document.getElementById('selectionError').innerHTML = ""
})