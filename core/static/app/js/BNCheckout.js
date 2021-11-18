// for showing the coupon apply form in buynow page......
document.getElementById('hacoupon').addEventListener('click', function () {
  let elm = document.getElementById('couponApply')
  elm.style.display = 'block'
  document.getElementById('hacoupon').style.display = 'none'
})
document.getElementById('cancelIcon').addEventListener('click', function () {
  document.getElementById('couponApply').style.display = 'none';
  document.getElementById('hacoupon').style.display = 'block'
})

// for increase or decrease the quantity of product on the buyNow page........
var quantity = document.getElementById('quantityValue')
var buyNowLeft = document.getElementById('buyNowLeft')
var quantityRightElm = document.getElementById("quantityRight")
var prodId = document.getElementById('minusBtn').getAttribute('prod')
var sellingPrizeElm = document.getElementById('sellPrizeElm')
var sellingPrize = sellingPrizeElm.getAttribute("sellingPrize")
var discountedPrizeElm = document.getElementById("discountedPrizeElm")
var discountedPrize = discountedPrizeElm.getAttribute("discountedPrize")
var subTotalElm = document.getElementById('subtotal')
var buyNowTotalElm = document.getElementById('buyNowTotal')
var couponErrorElm = document.getElementById('coupon_selector')
var hiddenCouponInfoElm = document.getElementById('hiddenCouponInfo')
var hiddenDiscountElm = document.getElementById('hiddenDiscount')
var hiddenNewTotalElm = document.getElementById('hiddenNewTotal')
var couponApplyElm = document.getElementById('couponApply')
var haveAnyCouponElm = document.getElementById('hacoupon')
var ProductGroup = document.getElementById('minusBtn').getAttribute('ProductGroup')
var unitAmount = document.getElementById('buyNowUnitAmount2')


function buyNow(elm) {
  var plusButton = document.getElementById('plusButton')
  var productStock = plusButton.getAttribute('productStock')
  var maxAmount = plusButton.getAttribute('maxAmount')
  // This section will work for product haveing solid and Liquid weight 
  if (ProductGroup == "SolidWeight" || ProductGroup == "LiquidWeight") {
    hiddenCouponInfoElm.style.display = 'none'
    couponApplyElm.style.display = 'none'
    haveAnyCouponElm.style.display = "block"
    if (elm == "plus") {
      Action = "plus"
    }
    if (elm == "minus") {
      Action = "minus"
    }
    $.ajax({
      method: "GET",
      url: "/buynowurl",
      data: {
        Group: "nonpacket",
        productId: prodId,
        action: Action
      },
      success: function (data) {
        unitAmount.innerHTML = data.unitAmount
        sellingPrizeElm.innerHTML = data.sellingCost
        discountedPrizeElm.innerHTML = data.discountedCost
        subTotalElm.innerHTML = data.discountedCost
        buyNowTotalElm.innerHTML = data.total
        document.getElementById('stockWarning').innerHTML = data.warning
      }
    })
  } 
  else
  // This section will work for packet product
  {
    // When user will click on the Plus button on the buynow page on packet Item this section will work
    if (elm == "plus") {
      quantityValue = parseInt(quantity.value) + 1
      quantity.value = quantityValue
      var quantityRightValue = parseInt(quantityRightElm.innerHTML) + 1
      quantityRightElm.innerHTML = quantityRightValue
      var newSellingPrize = parseInt(sellingPrize) * quantity.value
      sellingPrizeElm.innerHTML = newSellingPrize
      var newDiscountedPrize = discountedPrize * quantity.value
      discountedPrizeElm.innerHTML = newDiscountedPrize
      hiddenCouponInfoElm.style.display = 'none'
      couponApplyElm.style.display = 'none'
      haveAnyCouponElm.style.display = "block"

      if (quantityValue > productStock) {
        document.getElementById('stockWarning').innerHTML = "Stock out"
        plusButton.disabled = true
        document.getElementById('PTPBtn').disabled = true
        document.getElementById('PTPBtn').style.cursor = "not-allowed"
      }
    }

    // When user will click on the minus button on the buynow page this section will work
    if (elm == "minus") {
      quantityValue = parseInt(quantity.value) - 1
      quantity.value = quantityValue
      var quantityRightValue = parseInt(quantityRightElm.innerHTML) - 1;
      quantityRightElm.innerHTML = quantityRightValue;
      var newSellingPrize = parseInt(sellingPrize) * quantity.value
      sellingPrizeElm.innerHTML = newSellingPrize
      var newDiscountedPrize = discountedPrize * quantity.value
      discountedPrizeElm.innerHTML = newDiscountedPrize
      hiddenCouponInfoElm.style.display = 'none'
      couponApplyElm.style.display = 'none'
      haveAnyCouponElm.style.display = "block"
      // When quantity will be zero then the product will be hidden and delected...
      if (quantityValue == 0) {
        buyNowLeft.style.visibility = "hidden"
      }
      if (quantityValue <= productStock) {
        document.getElementById('stockWarning').innerHTML = ""
        plusButton.disabled = false
        document.getElementById('PTPBtn').disabled = false
        document.getElementById('PTPBtn').style.cursor = "pointer"
      }
    }
    $.ajax({
      method: "GET",
      url: "/buynowurl",
      data: {
        Group: "packet",
        productId: prodId,
        quantity: quantityValue
      },
      success: function (data) {
        subTotalElm.innerHTML = data.subTotal
        buyNowTotalElm.innerHTML = data.total
      }
    })
  }

  // When user will click on the Remove button on the buynow page this section will work
  if (elm == "remove") {
    buyNowLeft.style.visibility = 'hidden'
    hiddenCouponInfoElm.style.display = 'none'
    couponApplyElm.style.display = 'none'
    haveAnyCouponElm.style.display = "block"
  }
}

// When we will click on the apply button on the coupon apply form
document.getElementById('apply').addEventListener('click', function () {
  var code = document.getElementById('code').value
  $.ajax({
    method: "GET",
    url: '/bNVCheckerurl',
    data: {
      codeV: code
    },
    success: function (data) {
      couponErrorElm.innerHTML = data.message
      if (data.total != undefined) {
        hiddenCouponInfoElm.style.display = "block"
        hiddenDiscountElm.innerHTML = data.discount
        hiddenNewTotalElm.innerHTML = data.total
      } else {
        hiddenCouponInfoElm.style.display = 'none'
      }
    }
  })
})

// This Script will work on the changing the default address in checkout page on order summery. 
let adrEditElm = document.getElementById("adredit");
adrEditElm.addEventListener("click", adrEditFunc);

function adrEditFunc() {
  document.getElementById("ptp").innerText = "Select your shipping address";
  let editDiv = document.getElementById("editDiv");
  let adrDiv = document.getElementById("adrDiv");
  editDiv.style.display = "none";
  adrDiv.style.display = "block";
}
let clickChecker = document.getElementsByClassName("cHK");
let len = clickChecker.length;
for (let i = 0; i < len; i++) {
  clickChecker[i].addEventListener("click", function () {
    addrSelector(this);
  });
}

function addrSelector(elm) {
  document.getElementById("ptp").innerText = "Proceed To Pay";
  let sAdrDiv = document.getElementById("adrDiv");
  let odrSDiv = document.getElementById("editDiv");
  let adrId = elm.getAttribute("CAddressId");
  let checkedBox = document.getElementById("checked");
  checkedBox.style.display = "none";
  let circleBox = document.getElementsByClassName("isDefaultClass");
  let len = circleBox.length;
  for (let i = 0; i < len; i++) {
    if (circleBox[i].value == "True") {
      circleBox[i].style.display = "inline-block";
    }
  }
  $.ajax({
    type: "GET",
    url: "/sadrurl",
    data: {
      adrId: adrId,
    },
    success: function (data) {
      document.getElementById("shAdrName").innerText = data.name;
      document.getElementById(
        "adrWithLocations"
      ).innerText = `${data.address}, ${data.union}, ${data.upazila},${data.district}, ${data.division}`;
      console.log();
    },
  });
  sAdrDiv.style.display = "none";
  odrSDiv.style.display = "block";
}

// when the Checked Icon will be clicked then it will work...
document.getElementById("checked").addEventListener("click", function () {
  console.log("checked item has been clicked")
  document.getElementById("adrDiv").style.display = "none";
  document.getElementById("editDiv").style.display = "block";
});