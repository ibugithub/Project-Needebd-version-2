// // For to Know the which division user has been clicked
// function getdivision(element) {
//     let divName = document.getElementById('division').value
//     $.ajax({
//         type: "GET",
//         url: "/divsetterurl",
//         data: {
//             DivName: divName
//         },
//         success: function (data) {
//             document.getElementById('districts').disabled = false
//         }
//     })
// }

// // For filtering the district according to the selected division
// function districtsFilter() {
//     $.ajax({
//         type: "GET",
//         url: '/disfilterurl',
//         data: {},
//         success: function (data) {
//             let districtselms = document.getElementsByClassName('districts')
//             let len = districtselms.length
//             for (let i = 0; i < len; i++) {
//                 let fDistrictDivId = districtselms[i].getAttribute('divid');
//                 document.getElementById('opremove').style.display = 'none';
//                 if (fDistrictDivId != data.divId) {
//                     districtselms[i].style.display = 'none';
//                 } else {
//                     districtselms[i].style.display = 'block';
//                 }
//             }
//             document.getElementById('division').disabled = true
//         }
//     })
// }

// function getDistrictName() {
//     document.getElementById('upazilas').disabled = false;
//     let districtName = document.getElementById('districts').value
//     $.ajax({
//         type: "GET",
//         url: "/dissetterurl",
//         data: {
//             DistrictName: districtName
//         },
//         success: function (data) {}
//     })
// }

// function upazilaFilter() {
//     document.getElementById('opremove2').style.display = 'none'
//     console.log("im in upazila filter")
//     $.ajax({
//         type: 'GET',
//         url: '/upafilterurl',
//         success: function (data) {
//             let upazilaElements = document.getElementsByClassName('upazilas')
//             let len = upazilaElements.length
//             for (let i = 0; i < len; i++) {
//                 districtId = upazilaElements[i].getAttribute('district_id')
//                 if (districtId != data.districtId) {
//                     upazilaElements[i].style.display = 'none'
//                 } else {
//                     upazilaElements[i].style.display = 'block'
//                 }
//             }

//         }
//     })
// }



// for Filtering the districts.....
var districtSelect = document.createElement("Select")
districtSelect.setAttribute("disabled", "True")
districtSelect.setAttribute("class", "input-field")
districtSelect.setAttribute("id", "districtSelect")
districtSelect.setAttribute("class", "input-field")
districtSelect.setAttribute("onchange", "upazilaFilter()")
document.getElementById('districtDiv').appendChild(districtSelect)

function districtsFilter(){
    document.getElementById('districtSelect').disabled = false
    var divisionId1 = document.getElementById('divisions').value
    console.log("division1 id is", divisionId1)
    var allDistrictOptions = document.getElementsByClassName("allDistrictOptions") 
    let len = allDistrictOptions.length
    let previousOptions = document.getElementsByClassName('filteredDistricOption')
    if (previousOptions.length != 0){
        while(previousOptions[0]){
            previousOptions[0].remove()
        }
    }
    for (let i = 0; i < len; i++){
          var divisionId2 = allDistrictOptions[i].getAttribute('divisionId')
          console.log("divisionId2 is ", divisionId2)
          if (divisionId1 == divisionId2)
          {
            let option = document.createElement("option")
            option.setAttribute("class", "filteredDistricOption")
            let value = allDistrictOptions[i].innerHTML
            option.setAttribute("value", value)
            let innernode = document.createTextNode(value)
            option.appendChild(innernode)
            districtSelect.appendChild(option)
          }
    }
}


// for filtering the upazila ...
// creating a new select option....
var upazilaSelect = document.createElement("select")
upazilaSelect.setAttribute("class", "input-field")
upazilaSelect.setAttribute("id", "upazilaSelect")
upazilaSelect.setAttribute("disabled", "true")
document.getElementById('upazilaDiv').appendChild(upazilaSelect)

// creating the filtering function for upazila..
function upazilaFilter()
{   console.log("connected")
    document.getElementById('upazilaSelect').disabled = false


// write code from here ...





}





// for filtering the Unions according to the Upazila.....
var select = document.createElement("Select")
select.setAttribute("class", "input-field")
select.setAttribute("id", "unionSelect")
select.setAttribute("disabled", "True")
document.getElementById('uniondiv').appendChild(select)


function unionFilter() {
    // document.getElementById('unions').disabled = false
    upazilaId1 = document.getElementById('upazilas').value
    if (document.getElementsByClassName('unionoption').length != 0) {
        var prevoption = document.getElementsByClassName('unionoption')
        while(prevoption[0]){
            prevoption[0].remove()
        }
    }
    let unionElements = document.getElementsByClassName('unions')
    let len = unionElements.length
    for (let i = 0; i < len; i++) {
        upazilaId2 = unionElements[i].getAttribute('upazilaId')
        if (upazilaId1 == upazilaId2) {
            let val = unionElements[i].innerHTML
            let option = document.createElement("option")
            option.setAttribute('value', val)
            let node = document.createTextNode(val)
            option.setAttribute('class', 'unionoption')
            option.appendChild(node)
            document.getElementById('unionSelect').appendChild(option)
        }
    }
}
