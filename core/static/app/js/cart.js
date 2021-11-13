function PlusCart(element) {
    productGroup = element.getAttribute('ProductGroup')
    if (productGroup != 'SolidWeight' && productGroup != "LiquidWeight" && productGroup != "ClothPices") 
    {
    var quantityElm = element.parentNode.children[1].children[0];
    quantityValue = parseInt(quantityElm.value) + 1;
    quantityElm.value = quantityValue;
    quantityElm.innerHTML = quantityValue;
    }
    var prod_id = element.getAttribute('prod').toString()
    var c = element.getAttribute('flc')
    var tcid = ("tc" + c)
    var tProdCostElm = document.getElementById(tcid)
    var totalSellCostDom = document.getElementById('totalSellCostDom')
    var disCountDom = document.getElementById("discountDom")
    var totalCostDom = document.getElementById('totalCostDom')

    $.ajax({
        type: "GET",
        url: "/pluscarturl",
        data: {
            id: prod_id,
            unit: element.getAttribute('unit'),
            unit_amount: element.getAttribute('unit_amount'),
            size: element.getAttribute('size')
        },
        success: function (data) {
            if (productGroup == 'SolidWeight' || productGroup == "LiquidWeight" || productGroup == "ClothPices") 
            {
                var uAmountId = ("uamount" + c)
                var unitAmountElm = document.getElementById(uAmountId)
                unitAmountElm.innerHTML = data.unitAmount
            }
            tProdCostElm.innerHTML = data.products_total_cost
            totalSellCostDom.innerHTML = data.TotalSell_Cost
            disCountDom.innerHTML = data.Total_discount
            totalCostDom.innerHTML = data.Total_Cost
            document.getElementById('DDom').style.display = 'none'
        }
    })
}

function MinusCart(element) {
    var prod_id = element.getAttribute('prod').toString()
    productGroup = element.getAttribute('ProductGroup')
    var c = element.getAttribute('flc')
    var tcid = ("tc" + c)
    var tProdCostElm = document.getElementById(tcid)

    if (productGroup != 'SolidWeight' && productGroup != "LiquidWeight" && productGroup != "ClothPices") 
    {
        var quantityElm = element.parentNode.children[1].children[0]
        quantityValue = parseInt(quantityElm.value) - 1
        quantityElm.value = quantityValue
        quantityElm.innerHTML = quantityValue
    }
    var totalSellCostDom = document.getElementById('totalSellCostDom')
    var itemCounterDom = document.getElementById('ItemCountDom')
    var disCountDom = document.getElementById("discountDom")
    var totalCostDom = document.getElementById('totalCostDom')

    $.ajax({
        type: "GET",
        url: "/minuscarturl",
        data: {
            id: prod_id,
            unit: element.getAttribute('unit'),
            unit_amount: element.getAttribute('unit_amount'),
            size: element.getAttribute('size')
        },
        success: function (data) {
            if (data.quantity == 0) {
                element.parentNode.parentNode.parentNode.parentNode.style.display = 'none'
                var cartItemCount = document.getElementById('count')
                cartItemCount.innerHTML = data.cartCount
            }

            if (productGroup == 'SolidWeight' || productGroup == "LiquidWeight" || productGroup == "ClothPices") 
            {
                var uAmountId = ("uamount" + c)
                var unitAmountElm = document.getElementById(uAmountId)
                unitAmountElm.innerHTML = data.unitAmount
                if(data.deleted){
                    element.parentNode.parentNode.parentNode.parentNode.style.display = 'none'
                    var cartItemCount = document.getElementById('count')
                    cartItemCount.innerHTML = data.cartCount
                }
            }
            tProdCostElm.innerHTML = data.products_total_cost
            itemCounterDom.innerHTML = data.Item
            disCountDom.innerHTML = data.Total_discount
            totalSellCostDom.innerHTML = data.TotalSell_Cost
            totalCostDom.innerHTML = data.Total_Cost
            document.getElementById('DDom').style.display = 'none'
        }
    })
}

function RemoveCart(element) {
    element.parentNode.parentNode.parentNode.parentNode.style.display = 'none'
    var cartItemCount = document.getElementById('count')
    var totalSellCostDom = document.getElementById('totalSellCostDom')
    var totalCostDom = document.getElementById('totalCostDom')
    var itemCounterDom = document.getElementById('ItemCountDom')
    var disCountDom = document.getElementById("discountDom")

    $.ajax({
        method: "GET",
        url: '/removecarturl',
        data: {
            prod_id: element.getAttribute('prod_id'),
            unit: element.getAttribute('unit'),
            unit_amount: element.getAttribute('unit_amount'),
            size: element.getAttribute('size')

        },
        success: function (data) {
            cartItemCount.innerHTML = data.cartCount
            totalSellCostDom.innerHTML = data.TotalSell_Cost
            totalCostDom.innerHTML = data.Total_Cost
            itemCounterDom.innerHTML = data.Item
            disCountDom.innerHTML = data.Total_discount
            document.getElementById('DDom').style.display = 'none'
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