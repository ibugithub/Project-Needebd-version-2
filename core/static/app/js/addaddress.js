// For to Know the which division user has been clicked
function getdivision(element)
{
    let divName = document.getElementById('division').value
    $.ajax({
        type : "GET",
        url : "/divsetterurl",
        data : {
            DivName : divName
        },
        success: function(data){
            document.getElementById('districts').disabled = false
        }
    })
}

// For filtering the district according to the selected division
function districtsFilter(){
    $.ajax({
        type : "GET",
        url : '/disfilterurl',
        data : {
        },
        success : function(data){
            let districtselms = document.getElementsByClassName('districts')
            let len = districtselms.length
            for(let i = 0; i < len; i++){
                let fDistrictDivId = districtselms[i].getAttribute('divid');
                document.getElementById('opremove').style.display = 'none';
                if (fDistrictDivId != data.divId){
                    districtselms[i].style.display = 'none';
                }
                else{
                    districtselms[i].style.display = 'block';
                }
            }
            document.getElementById('division').disabled = true
        }
    })
}

function getDistrictName(){
    document.getElementById('upazilas').disabled = false;
    let districtName = document.getElementById('districts').value
    $.ajax({
        type : "GET",
        url : "/dissetterurl",
        data : {
            DistrictName : districtName
        },
        success: function(data){
        }
    })
}

function upazilaFilter()
{   document.getElementById('opremove2').style.display = 'none'
    $.ajax({
        type : 'GET',
        url : '/upafilterurl',
        success: function(data){
            let upazilaElements = document.getElementsByClassName('upazilas')
            let len = upazilaElements.length
            for (let i = 0; i < len; i++){
                districtId = upazilaElements[i].getAttribute('district_id')
                if (districtId != data.districtId)
                {
                    upazilaElements[i].style.display = 'none'
                }
                else{
                    upazilaElements[i].style.display = 'block'
                }
            }

        }
    })
}

function getUpazilaName(){
    let upazilaName = document.getElementById('upazilas').value
    $.ajax({
        type : 'GET',
        url : '/upasetterurl',
        data: {
            upazilaNamex : upazilaName
        }
    })

}

function unionFilter(){
    console.log('im here')
    $.ajax({
        type: 'GET',
        url : 'upaidgiverurl',

        success: function (){
            console.log("the id is",data.upazilaId)
        }
    })
}