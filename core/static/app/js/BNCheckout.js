// for showing the coupon apply form in buynow page......
document.getElementById('hacoupon').addEventListener('click', function(){
    let elm = document.getElementById('couponApply')
    elm.style.display = 'block'
    document.getElementById('hacoupon').style.display = 'none'
})
document.getElementById('cancelIcon').addEventListener('click', function(){
    document.getElementById('couponApply').style.display = 'none';
    document.getElementById('hacoupon').style.display = 'block'
})


// for increase or decrease the quantity of product........
var quantity = document.getElementById('quantityValue')
var buyNowLeft = document.getElementById('buyNowLeft')
var quantityRightElm = document.getElementById("quantityRight")

function PlusCart(elm){
    quantityValue = parseInt(quantity.value ) + 1
    quantity.value = quantityValue
    quantity.innerHTML = quantity.value
    
    var quantityRightValue = parseInt(quantityRightElm.innerHTML) + 1
    quantityRightElm.innerHTML = quantityRightValue
}

function MinusCart(elm){
    quantityValue = parseInt(quantity.value) - 1
    quantity.value = quantityValue
    quantity.innerHTML = quantity.value

    var quantityRightValue = parseInt(quantityRightElm.innerHTML) - 1;
    quantityRightElm.innerHTML = quantityRightValue;
    if (quantityRightValue == 0)
    {   
        buyNowLeft.style.visibility = "hidden"
    }
}


function RemoveCart(elm) {
    buyNowLeft.style.visibility = 'hidden'
}