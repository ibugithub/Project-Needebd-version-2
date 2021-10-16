// for Filtering the districts.....
var districtSelect = document.createElement("Select")
districtSelect.setAttribute("disabled", "True")
districtSelect.classList.add('input-field', 'errelm2')
districtSelect.setAttribute("id", "districtSelect")
districtSelect.setAttribute("name", "districtId")
districtSelect.setAttribute("onclick", "upazilaFilter()")

// I've create this section to save teh user's selected data after relode page.......
var datadistrictId = document.getElementById('dataGiver').getAttribute("districtId")
var datadistrictName = document.getElementById('dataGiver').getAttribute("districtName")
if (datadistrictName != "" && datadistrictId != "") {
    var dataOptions = document.createElement("option")
    dataOptions.setAttribute("value", datadistrictId)
    dataOptions.setAttribute("id", "psoption1")
    let innernode = document.createTextNode(datadistrictName)
    dataOptions.appendChild(innernode)
    districtSelect.removeAttribute('disabled')
    districtSelect.appendChild(dataOptions)
    document.getElementById('districtDiv').appendChild(districtSelect)
    districtsFilter()
}
// creating default options...
var defaultOptions = document.createElement("option")
defaultOptions.setAttribute("id", "defaultOption2")
defaultOptions.setAttribute("value", "default")
var node = document.createTextNode("select the district")
defaultOptions.appendChild(node)
districtSelect.appendChild(defaultOptions)

document.getElementById('districtDiv').appendChild(districtSelect)

var f = 1
function districtsFilter() {
    document.getElementById('districtSelect').disabled = false
    if (f == 1) {
        document.getElementById('defaultOption1').remove()
        if (datadistrictName != "" && datadistrictId != ""){
            document.getElementById("psoption1").remove()
        }
        
        f++
    }
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
upazilaSelect.classList.add('input-field', 'errelm2')
upazilaSelect.setAttribute("id", "upazilaSelect")
upazilaSelect.setAttribute("name", 'upazilaId')
upazilaSelect.setAttribute("disabled", "true")
upazilaSelect.setAttribute("onclick", "unionFilter()")

// I've create this section to save teh user's selected data after relode page.......
var dataUpazilaId = document.getElementById('dataGiver').getAttribute("upazilaId")
var dataUpazilaName = document.getElementById('dataGiver').getAttribute("upazilaName")
if (dataUpazilaName != "" && dataUpazilaId != "") {
    var dataOptions = document.createElement("option")
    dataOptions.setAttribute("id", "psoption2")
    dataOptions.setAttribute("value", dataUpazilaId)
    let innernode = document.createTextNode(dataUpazilaName)
    dataOptions.appendChild(innernode)
    upazilaSelect.removeAttribute('disabled')
    upazilaSelect.appendChild(dataOptions)
    document.getElementById('upazilaDiv').appendChild(upazilaSelect)
    upazilaFilter()
}

// creating default options...
var defaultOptions = document.createElement("option")
defaultOptions.setAttribute("id", "defaultOption3")
defaultOptions.setAttribute("value", "default")
var node = document.createTextNode("select the upazila")
defaultOptions.appendChild(node)
upazilaSelect.appendChild(defaultOptions)

document.getElementById('upazilaDiv').appendChild(upazilaSelect)

// creating the filtering function for upazila..
var f2 = 1

function upazilaFilter() {    
    document.getElementById('upazilaSelect').disabled = false
    if (f2 == 1) {
        document.getElementById("defaultOption2").remove()
        if (dataUpazilaName != "" && dataUpazilaId != ""){
            document.getElementById("psoption2").remove()
        }
        f2++
    }
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
select.classList.add('input-field', 'errelm2')
select.setAttribute("id", "unionSelect")
select.setAttribute("name", "unionId")
select.setAttribute("disabled", "True")
select.setAttribute("onclick", "dOption4Remover()")

// I've create this section to save teh user's selected data after relode page.......
var dataUnionId = document.getElementById('dataGiver').getAttribute("unionId")
var dataUnionName = document.getElementById('dataGiver').getAttribute("unionName")
if (dataUnionName != "" && dataUnionId != "") {
    var dataOptions = document.createElement("option")
    dataOptions.setAttribute("id", "psoption3")
    dataOptions.setAttribute("value", dataUnionId)
    let innernode = document.createTextNode(dataUnionName)
    dataOptions.appendChild(innernode)
    select.removeAttribute('disabled')
    select.appendChild(dataOptions)
    document.getElementById('uniondiv').appendChild(select)
    unionFilter()
}

// creating default options...
var defaultOptions = document.createElement("option")
defaultOptions.setAttribute("id", "defaultOption4")
defaultOptions.setAttribute("value", "default")
var node = document.createTextNode("select the union")
defaultOptions.appendChild(node)
select.appendChild(defaultOptions)

document.getElementById('uniondiv').appendChild(select)

var f3 = 1
function unionFilter() {    
    document.getElementById('unionSelect').disabled = false
    if (f3 == 1) {
        document.getElementById('defaultOption3').remove()
        if (dataUnionName != "" && dataUnionId != ""){
            document.getElementById('psoption3').remove()
        }

        f3++
    }
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

let f4 = 1
function dOption4Remover() {
    if (f4 == 1) {
        document.getElementById("defaultOption4").remove()
        f4++
    }
}

// Validating all the inputs..
errorElm = document.getElementsByClassName('errelm')
let len = errorElm.length
for (let i = 0; i < len; i++) {
    errorElm[i].addEventListener("change", function () {
        errorRemover(this)
    })
}
errorElm2 = document.getElementsByClassName('errelm2')
let len2 = errorElm2.length
for (let i = 0; i < len2; i++) {
    errorElm2[i].addEventListener('click', function () {
        errorRemover(this)
    })
}

function errorRemover(elm) {
    elm.parentNode.childNodes[3].style.display = 'none'
    if (elm.value == "") {
        elm.parentNode.childNodes[3].style.display = 'block'
    }
}