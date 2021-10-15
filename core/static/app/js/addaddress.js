// This function Will handle the default Options when to hide and show the default options...
function DOptionRemover(elm, param) {
    if (param == "diff") {
        elm.childNodes[1].style.visibility = 'hidden'
    } else {
        elm.childNodes[0].style.visibility = 'hidden'
    }
    // elm.parentNode.childNodes[3].style.display = 'none'
}

// for Filtering the districts.....
var districtSelect = document.createElement("Select")
districtSelect.setAttribute("disabled", "True")
districtSelect.classList.add('input-field', 'errelm')
districtSelect.setAttribute("id", "districtSelect")
districtSelect.setAttribute("name", "districtId")
districtSelect.setAttribute("onclick", "DOptionRemover(this, 'nodiff')")
districtSelect.setAttribute("onchange", "upazilaFilter()")
// creating default options...
var defaultOptions = document.createElement("option")
defaultOptions.setAttribute("value", "default")
var node = document.createTextNode("select the district")
defaultOptions.appendChild(node)
districtSelect.appendChild(defaultOptions)

document.getElementById('districtDiv').appendChild(districtSelect)

function districtsFilter() {
    document.getElementById('districtSelect').disabled = false
    document.getElementById('defaultOption1').style.display = 'none'
    var divisionId1 = document.getElementById('divisions').value
    var allDistrictOptions = document.getElementsByClassName("allDistrictOptions")
    let len = allDistrictOptions.length
    let previousOptions = document.getElementsByClassName('filteredDistricOption')
    if (previousOptions.length != 0) {
        while (previousOptions[0]) {
            previousOptions[0].remove()
        }
    }
    for (let i = 0; i < len; i++) {
        var divisionId2 = allDistrictOptions[i].getAttribute('divisionId')
        if (divisionId1 == divisionId2) {
            let option = document.createElement("option")
            option.setAttribute("class", "filteredDistricOption")
            let value1 = allDistrictOptions[i].value
            let value2 = allDistrictOptions[i].innerHTML
            option.setAttribute("value", value1)
            let innernode = document.createTextNode(value2)
            option.appendChild(innernode)
            districtSelect.appendChild(option)
        }
    }
}


// for filtering the upazila ...
// creating a new select option....
var upazilaSelect = document.createElement("select")
upazilaSelect.classList.add('input-field', 'errelm')
upazilaSelect.setAttribute("id", "upazilaSelect")
upazilaSelect.setAttribute("name", 'upazilaId')
upazilaSelect.setAttribute("disabled", "true")
upazilaSelect.setAttribute("onchange", "unionFilter()")
upazilaSelect.setAttribute("onclick", "DOptionRemover(this, 'notdiff')")
// creating default options...
var defaultOptions = document.createElement("option")
defaultOptions.setAttribute("value", "default")
var node = document.createTextNode("select the upazila")
defaultOptions.appendChild(node)
upazilaSelect.appendChild(defaultOptions)

document.getElementById('upazilaDiv').appendChild(upazilaSelect)

// creating the filtering function for upazila..
function upazilaFilter() {
    document.getElementById('upazilaSelect').disabled = false
    var districtId1 = document.getElementById('districtSelect').value
    var AllUpazilaOptions = document.getElementsByClassName('AllUpazilaOptions')
    let len = AllUpazilaOptions.length
    let previousOptions = document.getElementsByClassName('filteredUpazilaOptions')
    if (previousOptions.length != 0) {
        while (previousOptions[0]) {
            previousOptions[0].remove()
        }
    }
    for (let i = 0; i < len; i++) {
        districtId2 = AllUpazilaOptions[i].getAttribute('districtId')
        if (districtId1 == districtId2) {
            let option = document.createElement('option')
            option.setAttribute('class', "filteredUpazilaOptions")
            let value1 = AllUpazilaOptions[i].value
            let value2 = AllUpazilaOptions[i].innerHTML
            option.setAttribute("value", value1)
            let innernode = document.createTextNode(value2)
            option.appendChild(innernode)
            upazilaSelect.appendChild(option)
        }
    }
}


// for filtering the Unions according to the Upazila.....
var select = document.createElement("Select")
select.classList.add('input-field', 'errelm')
select.setAttribute("id", "unionSelect")
select.setAttribute("name", "unionId")
select.setAttribute("disabled", "True")
select.setAttribute("onclick", "DOptionRemover(this, 'notdiff')")
// creating default options...
var defaultOptions = document.createElement("option")
defaultOptions.setAttribute("value", "default")
var node = document.createTextNode("select the union")
defaultOptions.appendChild(node)
select.appendChild(defaultOptions)

document.getElementById('uniondiv').appendChild(select)

function unionFilter() {
    document.getElementById('unionSelect').disabled = false
    upazilaId1 = document.getElementById('upazilaSelect').value
    let previousOption = document.getElementsByClassName('unionoption')
    if (document.getElementsByClassName('unionoption').length != 0) {
        while (previousOption[0]) {
            previousOption[0].remove()
        }
    }
    let unionElements = document.getElementsByClassName('unions')
    let len = unionElements.length
    for (let i = 0; i < len; i++) {
        upazilaId2 = unionElements[i].getAttribute('upazilaId')
        if (upazilaId1 == upazilaId2) {
            let option = document.createElement("option")
            option.setAttribute('class', 'unionoption')
            let val1 = unionElements[i].value
            let val2 = unionElements[i].innerHTML
            option.setAttribute('value', val1)
            let innernode = document.createTextNode(val2)
            option.appendChild(innernode)
            document.getElementById('unionSelect').appendChild(option)
        }
    }
}


// Validating all the inputs..

errorElm = document.getElementsByClassName('errelm')
console.log(errorElm)
let len = errorElm.length
for (let i = 0; i < len; i++) {
    errorElm[i].addEventListener("change", function () {
        errorRemover(this)
    })
    console.log(errorElm[i])
}

function errorRemover(elm) {
    elm.parentNode.childNodes[3].style.display = 'none'
}
