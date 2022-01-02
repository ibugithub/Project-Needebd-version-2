var button = document.getElementsByClassName("PTCOB")
var buttonLen = button.length
var stockWarningElm = document.getElementsByClassName('stockWarning')

function PlusCart(element) {
    ProductType= element.getAttribute('ProductGroup')
    var c = element.getAttribute('flc')
    var tcid = ("tc" + c)
    var quantityElmId = ("quantity" + c)
    var stockWarningId = ("stockWarning" + c)
    var plusButton = document.getElementById("plusCart" + c)
    var stockWarningElm = document.getElementById(stockWarningId)
    var tProdCostElm = document.getElementById(tcid)
    productStock = parseFloat(element.getAttribute('productStock'))
    if (ProductType!= 'SolidWeight' && ProductType!= "LiquidWeight" && ProductType!= "ClothPices") 
    {
    var quantityElm = document.getElementById(quantityElmId)

    quantityValue = parseInt(quantityElm.value)
    if (quantityValue > productStock)
    {  
        plusButton.disabled = true
    }
    else{
        quantityElm.value = quantityValue + 1;  
    }
    }
    var prod_id = element.getAttribute('prod').toString()
    var totalSellCostDom = document.getElementById('totalSellCostDom')
    var disCountDom = document.getElementById("discountDom")
    var totalCostDom = document.getElementById('totalCostDom')
    var totalCostDomM = document.getElementById('totalCostDomM')
    
    $.ajax({
        type: "GET",
        url: "/pluscarturl",
        data: {
            id: prod_id,
            unit: element.getAttribute('unit'),
            size: element.getAttribute('size')
        },
        success: function (data) {
            if (ProductType== 'SolidWeight' || ProductType== "LiquidWeight" || ProductType== "ClothPices") 
            {
                var uAmountId = ("uamount" + c)
                var unitAmountElm = document.getElementById(uAmountId)
                unitAmountElm.innerHTML = data.unitAmount
            }
            tProdCostElm.innerHTML = data.products_total_cost
            totalSellCostDom.innerHTML = data.TotalSell_Cost
            disCountDom.innerHTML = data.Total_discount
            totalCostDom.innerHTML = data.Total_Cost
            totalCostDomM.innerHTML = data.Total_Cost
            stockWarningElm.innerHTML = data.warning
            document.getElementById('DDom').style.display = 'none'
        }
    })
}
function MinusCart(element) {
    var prod_id = element.getAttribute('prod').toString()
    ProductType= element.getAttribute('ProductGroup')
    var c = element.getAttribute('flc')
    var tcid = ("tc" + c)
    var quantityElmId = ("quantity" + c) 
    var quantityElmId = ("quantity" + c) 
    var stockWarningId = ("stockWarning" + c)
    var stockWarningElm = document.getElementById(stockWarningId)
    var plusButton = document.getElementById("plusCart" + c)
    var tProdCostElm = document.getElementById(tcid)
    productStock = parseFloat(element.getAttribute('productStock'))
    if (ProductType!= 'SolidWeight' && ProductType!= "LiquidWeight" && ProductType!= "ClothPices") 
    {
        var quantityElm = document.getElementById(quantityElmId)
        quantityValue = parseInt(quantityElm.value)

        quantityValue = parseInt(quantityElm.value) - 1
        quantityElm.value = quantityValue

        plusButton.disabled = false
        if (quantityValue <= productStock){
            for (let i = 0; i < buttonLen; i++){
            button[i].disabled = false
            button[i].style.cursor = "pointer" 
            }
            
        }
    }
    var totalSellCostDom = document.getElementById('totalSellCostDom')
    var itemCounterDom = document.getElementById('ItemCountDom')
    var disCountDom = document.getElementById("discountDom")
    var totalCostDom = document.getElementById('totalCostDom')
    var totalCostDomM = document.getElementById('totalCostDomM')
    $.ajax({
        type: "GET",
        url: "/minuscarturl",
        data: {
            id: prod_id,
            unit: element.getAttribute('unit'),
            size: element.getAttribute('size')
        },
        success: function (data) {
            if (data.quantity == 0) 
            {
                element.parentNode.parentNode.parentNode.parentNode.style.display = 'none'
                var cartItemCount = document.getElementById('count')
                cartItemCount.innerHTML = data.cartCount
            }
            if (ProductType== 'SolidWeight' || ProductType== "LiquidWeight" || ProductType== "ClothPices"){
                stockWarningElm.innerHTML = ""
                var uAmountId = ("uamount" + c)
                var unitAmountElm = document.getElementById(uAmountId)
                unitAmountElm.innerHTML = data.unitAmount
                for (let i = 0; i < buttonLen; i++){
                    button[i].disabled = false
                    button[i].style.cursor = "pointer" 
                    }

            } 
            tProdCostElm.innerHTML = data.products_total_cost
            itemCounterDom.innerHTML = data.Item
            disCountDom.innerHTML = data.Total_discount
            totalSellCostDom.innerHTML = data.TotalSell_Cost
            totalCostDom.innerHTML = data.Total_Cost
            totalCostDomM.innerHTML = data.Total_Cost
            document.getElementById('DDom').style.display = 'none'
            stockWarningElm.innerHTML = data.warning
        }
    })
}
function RemoveCart(element) {
    element.parentNode.parentNode.parentNode.parentNode.style.display = 'none'
    var cartItemCount = document.getElementById('count')
    var totalSellCostDom = document.getElementById('totalSellCostDom')
    var totalCostDom = document.getElementById('totalCostDom')
    var totalCostDomM = document.getElementById('totalCostDomM')
    var itemCounterDom = document.getElementById('ItemCountDom')
    var disCountDom = document.getElementById("discountDom")
    var c = element.getAttribute('flc')
    var stockWarningId = ("stockWarning" + c)
    document.getElementById(stockWarningId).innerHTML = ""
    for (let i = 0; i < buttonLen; i++){
        button[i].disabled = false
        button[i].style.cursor = "pointer" 
        }
    $.ajax({
        method: "GET",
        url: '/removecarturl',
        data: {
            prod_id: element.getAttribute('prod_id'),
            unit: element.getAttribute('unit'),
            size: element.getAttribute('size')
        },
        success: function (data) {
            cartItemCount.innerHTML = data.cartCount
            totalSellCostDom.innerHTML = data.TotalSell_Cost
            totalCostDom.innerHTML = data.Total_Cost
            totalCostDomM.innerHTML = data.Total_Cost
            itemCounterDom.innerHTML = data.Item
            disCountDom.innerHTML = data.Total_discount
            document.getElementById('DDom').style.display = 'none'
            document.getElementById("aTCD").style.display = "none"
        }
    })
}
document.getElementById('apply').addEventListener('click', voucherChecker)
function voucherChecker() {
    codedom = document.getElementById('code').value
    $.ajax({
        method: "GET",
        url: '/vcurl',
        data: {
            code: codedom
        },
        success: function (data) {
            DMDom = document.getElementById('DMDom')
            if (data.total_amount != "Nan") {
                document.getElementById('DDom').style.display = 'block'
                document.getElementById('DADom').innerHTML = data.discount
                document.getElementById('NADom').innerHTML = data.total_amount
                DMDom.style.display = "block"
                DMDom.innerHTML = data.message
                document.getElementById('code').value = ""

            } else {
                DMDom.style.display = "block"
                document.getElementById('DDom').style.display = 'none'
                DMDom.innerHTML = data.message
            }
        }
    })
}

// This function will prevent you from checking out if one of carted product has been stock out
for (let i = 0; i < buttonLen; i++)
{
   button[i].addEventListener('mouseover', function() {
    let len = stockWarningElm.length
    for (let i = 0; i < len; i++){
        
        if(stockWarningElm[i].innerHTML != ""){
            var stock = true
        }
        if (stock == true){
            for (let i = 0; i < buttonLen; i++){
                button[i].disabled = true
                button[i].style.cursor = "not-allowed" 
            }
        }
    }
}) 
}



