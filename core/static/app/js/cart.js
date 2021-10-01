function addToCart(element){
    console.log("addToCart Function has been clalled")
    let prod_id = element.getAttribute('prod')
    console.log(prod_id)
    try {
        unit = document.getElementById('unit').value
    }
    catch{
        unit = "-"
    }
    try{
        unit_amount = document.getElementById('unitAmount').value
    }
    catch{
        unit_amount = "-"
    }
    try{
         size = document.getElementById('size').value
    }
    catch {
        size = "-"
    }
    console.log("This is the Unit amount", unit_amount)
    console.log("This is the Unit", unit)
    console.log("This is the size", size)
    $.ajax({
        method : "GET",
        url : '/addtocarturl/',
        data : {
            productid : prod_id,
            unit : unit,
            unit_amount : unit_amount,
            Size : size
        },
        success: function(){

            console.log("Successfully returned back ")
        }
    })
}

function PlusCart(element)
{ 
    var prod_id = element.getAttribute('prod').toString()
    var c = element.getAttribute('flc')
    var tcid = ("tc"+c)
    var tProdCostElm = document.getElementById(tcid)
    
    $.ajax({
        type : "GET",
        url  : "/pluscarturl",
        data : {
            id : prod_id,
            unit : element.getAttribute('unit'),
            unit_amount : element.getAttribute('unit_amount'),
            size : element.getAttribute('size')

        },
        success: function(data){
            var quantityElm = element.parentNode.children[1].children[0]        
            quantityElm.value  = data.quantity
            tProdCostElm.innerHTML = data.total_products_cost
        }
    })
}

function MinusCart(element)
{    
    var prod_id = element.getAttribute('prod').toString()
    console.log(prod_id)
    var c = element.getAttribute('flc')
    var tcid = ("tc"+c)
    var tProdCostElm = document.getElementById(tcid)

    $.ajax({
        type : "GET",
        url  : "/minuscarturl",
        data : {
            id : prod_id,
            unit : element.getAttribute('unit'),
            unit_amount : element.getAttribute('unit_amount'),
            size : element.getAttribute('size')
        },
        success: function(data){
            console.log(data.quantity)
            if (data.quantity == 0){
                console.log('you should delete it')
                element.parentNode.parentNode.parentNode.parentNode.style.display = 'none'
                var cartItemCount = document.getElementById('count')
                cartItemCount.innerHTML = data.cartCount
            }
            var quantityElm = element.parentNode.children[1].children[0]
            quantityElm.value  = data.quantity
            tProdCostElm.innerHTML = data.total_products_cost
        }
    })
}

function RemoveCart(element)
{
    element.parentNode.parentNode.parentNode.parentNode.style.display = 'none'
    $.ajax({
        method : "GET",
        url : '/removecarturl',
        data : {
            prod_id : element.getAttribute('prod_id'),
            unit : element.getAttribute('unit'),
            unit_amount : element.getAttribute('unit_amount'),
            size : element.getAttribute('size')

        },
        success: function(data){
            var cartItemCount = document.getElementById('count')
            var count = data.cartCount
            cartItemCount.innerHTML =data.cartCount
        }

        
    })
}

