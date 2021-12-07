fullName = document.getElementById("fullName")
nameError = document.getElementById('nameError')
phone = document.getElementById('phoneNumber')
phoneError = document.getElementById("phoneError")
saveButton = document.getElementById('saveBtn')
divisionSelect = document.getElementById("divisions")
districtSelect = document.getElementById('districts')
upazilaSelect = document.getElementById('upazilas')
unionSelect = document.getElementById('unions')
address = document.getElementById('address')


// For filtering the distric, upazilla and union according to the selected option
divisionSelect.addEventListener('change', e=> {
    districtSelect.disabled = false
    const selectedDivision = e.target.value
    districtSelect.innerHTML = ""

    const option = document.createElement("option")
    option.textContent = 'select The district'
    option.setAttribute('value', "default")
    districtSelect.appendChild(option) 

    $.ajax({
        type : "GET",
        url : `/distric_data_url/${selectedDivision}/`,
        success: function(response){
            const districtsData = response.data
            districtsData.map(item=>{
                const option = document.createElement("option")
                option.textContent = item.name
                option.setAttribute('value', item.id)
                districtSelect.appendChild(option) 
            })
        },
        error: function(error) {
            console.log(error)
        }
    })
})

districtSelect.addEventListener('change', e=> {
    upazilaSelect.disabled = false
    const selectedDistrict = e.target.value
    upazilaSelect.innerHTML = ""
    
    const option = document.createElement("option")
    option.textContent = 'select The upazila'
    option.setAttribute('value', "default")
    upazilaSelect.appendChild(option) 

    $.ajax({
        type : "GET",
        url : `/upazila_data_url/${selectedDistrict}/`,
        success: function(response){
            const upazilasData = response.data
            upazilasData.map(item=>{
                const option = document.createElement("option")
                option.textContent = item.name
                option.setAttribute('value', item.id)
                upazilaSelect.appendChild(option) 
            })
        },
        error: function(error) {
            console.log(error)
        }
    })
})

upazilaSelect.addEventListener('change', e=> {
    unionSelect.disabled = false

    const selectedUpazila = e.target.value
    unionSelect.innerHTML = ""

    const option = document.createElement("option")
    option.textContent = 'select The union'
    option.setAttribute('value', "default")
    unionSelect.appendChild(option) 

    $.ajax({
        method: "GET",
        url : `/union_data_url/${selectedUpazila}/`,
        success: function(response){
            const unionsData = response.data
            unionsData.map(item=>{
                const option = document.createElement("option")
                option.textContent = item.name
                option.setAttribute('value', item.id)
                unionSelect.appendChild(option) 
            })
        }
    })
})



// validating function before sending it to the backend
if(saveButton){
  saveButton.addEventListener("mouseover", validationFunc)  
}
updateButton = document.getElementById('updateBtn')
if (updateButton){
  updateButton.addEventListener("mouseover", validationFunc)  
}

function validationFunc(){

    if (fullName.value == ""){
        nameError.innerHTML = "you must write a name"
        attempt1 = false
        if (updateButton){
            updateButton.disabled = true
        }
        if(saveButton){
            saveButton.disabled = true 
        }
    }

    if (phone.value == ""){
        phoneError.innerHTML = "you must write a phone number "
        attempt2 = false
        if (updateButton){
            updateButton.disabled = true
        }
        if(saveButton){
            saveButton.disabled = true 
        }
    }


    if (divisionSelect.value == "" || divisionSelect.value == "default"){
        diverror.innerHTML = "you must select a division"
        attempt3 = false
        if (updateButton){
            updateButton.disabled = true
        }
        if(saveButton){
            saveButton.disabled = true 
        }
    }


    if (districtSelect.value == "" || districtSelect.value == "default"){
        diserror.innerHTML = "you must select a district"
        attempt4 = false
        if (updateButton){
            updateButton.disabled = true
        }
        if(saveButton){
            saveButton.disabled = true 
        }
    }


    if (upazilaSelect.value == "" || upazilaSelect.value == "default"){
        upaerror.innerHTML = "you must select a upazilla"
        attempt5 = false
        if (updateButton){
            updateButton.disabled = true
        }
        if(saveButton){
            saveButton.disabled = true 
        }
    }


    if (unionSelect.value == "" || unionSelect.value == "default"){
        unionerror.innerHTML = "you must select a union"
        attempt6 = false
        if (updateButton){
            updateButton.disabled = true
        }
        if(saveButton){
            saveButton.disabled = true 
        }
    }


    if (address.value == "" || address.value == "default"){
        addrerror.innerHTML = "you must write a address"
        attempt7 = false
        if (updateButton){
            updateButton.disabled = true
        }
        if(saveButton){
            saveButton.disabled = true 
        }
    }
    
}

// Validating all the inputs..
allInput = document.getElementsByClassName('input-field') 
inputLen = allInput.length 
for (let i = 0; i < inputLen; i++)  {
    allInput[i].addEventListener("change", function(){
        if (allInput[i].value != "")
        {
            if(saveButton){
                saveButton.disabled = false
              }

              if (updateButton){
                updateButton.disabled = false
            }
        }
        errorRemover(this)
    })
}


function errorRemover(elm) {
    elm.parentNode.childNodes[3].style.display = 'none'
    if (elm.value == "" || elm.value == "default") {
        elm.parentNode.childNodes[3].style.display = 'block'
    }
}