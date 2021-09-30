
//---------- This is the start sing in java scripts----------------//

const email = document.forms['form']['email']
const password = document.forms['form']['password']

const emailError = document.querySelector('.email-error')
const passwordError = document.querySelector('.password-error')

email.addEventListener('textInput', emailVerify)
password.addEventListener('textInput', passwordVerify)

function validated(){
    if(email.value.length <9 ){
       emailError.style.display = "block"
       email.focus();
        return false ;
    }
    if(password.value.length <9 ){
        passwordError.style.display = "block"
        password.focus()
         return false ;
     }
     
}

function emailVerify(){
    if(email.value.length >= 8){
        emailError.style.display = "none"
        email.focus();
         return true;
    }
}

function passwordVerify(){
    if(password.value.length >= 8){
        passwordError.style.display = "none"
        email.focus();
         return true;
    }
}




