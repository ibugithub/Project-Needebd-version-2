// single page zooming section 
function imageZoom(imgID, resultID) {
  var img, lens, result, cx, cy;
  img = document.getElementById(imgID);
  result = document.getElementById(resultID);
  /*create lens:*/
  lens = document.createElement("DIV");
  lens.setAttribute("class", "img-zoom-lens");
  /*insert lens:*/
  img.parentElement.insertBefore(lens, img);
  /*calculate the ratio between result DIV and lens:*/
  cx = result.offsetWidth / lens.offsetWidth;
  cy = result.offsetHeight / lens.offsetHeight;
  /*set background properties for the result DIV:*/
  result.style.backgroundImage = "url('" + img.src + "')";
  result.style.backgroundSize = (img.width * cx) + "px " + (img.height * cy) + "px";
  /*execute a function when someone moves the cursor over the image, or the lens:*/
  lens.addEventListener("mousemove", moveLens);
  img.addEventListener("mousemove", moveLens);
  /*and also for touch screens:*/
  lens.addEventListener("touchmove", moveLens);
  img.addEventListener("touchmove", moveLens);

  /*initialise and hide lens result*/
  result.style.display = "none";
  /*Reveal and hide on mouseover or out*/
  lens.onmouseover = function () {
    result.style.display = "block";
  };
  lens.onmouseout = function () {
    result.style.display = "none";
  };

  function moveLens(e) {
    var pos, x, y;
    /*prevent any other actions that may occur when moving over the image:*/
    e.preventDefault();
    /*get the cursor's x and y positions:*/
    pos = getCursorPos(e);
    /*calculate the position of the lens:*/
    x = pos.x - (lens.offsetWidth / 2);
    y = pos.y - (lens.offsetHeight / 2);
    /*prevent the lens from being positioned outside the image:*/
    if (x > img.width - lens.offsetWidth) {
      x = img.width - lens.offsetWidth;
    }
    if (x < 0) {
      x = 0;
    }
    if (y > img.height - lens.offsetHeight) {
      y = img.height - lens.offsetHeight;
    }
    if (y < 0) {
      y = 0;
    }
    /*set the position of the lens:*/
    lens.style.left = x + "px";
    lens.style.top = y + "px";
    /*display what the lens "sees":*/
    result.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
  }

  function getCursorPos(e) {
    var a, x = 0,
      y = 0;
    e = e || window.event;
    /*get the x and y positions of the image:*/
    a = img.getBoundingClientRect();
    /*calculate the cursor's x and y coordinates, relative to the image:*/
    x = e.pageX - a.left;
    y = e.pageY - a.top;
    /*consider any page scrolling:*/
    x = x - window.pageXOffset;
    y = y - window.pageYOffset;
    return {
      x: x,
      y: y
    };
  }
};

imageZoom("myimage", "myresult");

var preview = document.getElementsByClassName('pretend_view');
var images = document.getElementById('pretend_images');
var thumbnails = document.querySelectorAll('#pretend_images > div');

thumbnails.forEach(function (elem) {
  elem.onclick = onClick.bind(null, elem);
});

function onClick(elem, e) {
  clearPreview();
  addToPreview(elem);
}

function clearPreview() {
  var elem = document.querySelector('.preview');

  if (elem) {
    elem.className = elem.className.replace('preview', '');
    images.appendChild(elem);
  }
}

function addToPreview(elem) {
  elem.className = 'preview';
  preview.appendChild(elem);
}

// controling the unit size etc
// this function will take the unit amount and size of the product and send it to the backend
function addToCart(element) {
  let prod_id = element.getAttribute('prod')
  try {
    unit = document.getElementById('unit').value
  } catch {
    unit = "-"
  }
  try {
    unit_amount = document.getElementById('unitAmount').value
  } catch {
    unit_amount = "-"
  }
  try {
    size = document.getElementById('size').value
  } catch {
    size = "-"
  }
  $.ajax({
    method: "GET",
    url: '/addtocarturl/',
    data: {
      productid: prod_id,
      unit: unit,
      unit_amount: unit_amount,
      Size: size
    },
    success: function () {
      document.getElementById('Rproduct').style.display = "none"
      document.getElementById('Sproduct').style.display = 'block'
    }
  })
}

// This function will Show the different unit and size on the fontend according to the product 
function fput() {
  let emptydiv = document.getElementById("EmptyDiv");
  let unitGroup = emptydiv.getAttribute("unitGroup");

  let ClothObj = ` <div class="color-size">
    <div id = "unitAlert" style = "color: red; display: none;"> <span > slect the Size </span> </div>
      <div class="p-size">
        <div class="p-size-text">
          <span >Size:</span>
        </div>
        <div class="size-button">
          <select onchange = "uAmountCk()"  id = "size" class="size-button-btn" name = "unit">
          <option value = "select">Select</option>
            <option value = "small">Small</option>
            <option value = "medium">Medium</option>
            <option value = "large"> Large </option>
          </select>
        </div>
      </div>
    </div>`;

  let ClothPicesObj = ` <div class="color-size">
  <div id = "unitAlert" style = "color: red; display: none;"> <span > slect the unit </span> </div>
        <div class="p-size">
          <div class="p-size-text">
            <span >Unit:</span>
          </div>
          <div class="size-button">
            <select  id = "unit" onchange = "uAmountCk()" class="size-button-btn" name = "unit">
              <option value = "select">Select</option>
              <option value = "SqureMeter"> Squre Meter </option>
              <option value = "SqureYeard"> Squre Yeard </option>             
            </select>
          </div>
        </div>
      <div id = "sAlert" style = "color: red; display: none;"> <span > slect the amount </span> </div>
      <div> 
        <label style = " color : #444;" for = "unitAmount" > Amount: </label>
        <input id = "unitAmount" onchange = "uAmountCk()"  type = "number" value = "">
      </div>
    </div>`;

  let ShoeSizeUnit = ` <div class="color-size">
  <div id = "unitAlert" style = "color: red; display: none;"> <span > select the size </span> </div>
  <div class="p-size">
    <div class="p-size-text">
      <span >Size:</span>
    </div>
    <div class="size-button">
      <select  id = "size" onchange = "uAmountCk()" class="size-button-btn" name = "unit">
      <option value = "select">Select</option>
        <option value = "41">41</option>
        <option value = "42">42</option>
        <option value = "43"> 43 </option>
        <option value = "44">44</option>
        <option value = "45">45</option>
        <option value = "46"> 46 </option>
      </select>
    </div>
  </div>
</div>`;

  let KgUnit = ` <div class="color-size">
  <div  id = "unitAlert" style = "color: red; display: none;"> <span > slect the unit </span> </div>
  <div class="p-size">
    <div class="p-size-text">
      <span >Weight:</span>
    </div>
    <div class="size-button">
      <select onchange = "uAmountCk()"  id = "unit" class="size-button-btn" name = "unit">
        <option value = "select">Select</option>
        <option value = "Kg"> Kg </option>
        <option value = "Gram"> Gram </option>
        <option value = "Pound"> Pound </option>
      </select> <br> 
    </div>
  </div>
  <div id = "sAlert" style = "color: red; display: none;"> <span > slect the amount </span> </div>
  <div> 
    <label style = " color : #444;" for = "unitAmount" > Amount: </label>
    <input id = "unitAmount" onchange = "uAmountCk()"  type = "number" value = "">
  </div>
  </div>`;

  let LiterUnit = ` <div class="color-size">
  <div id = "unitAlert" style = "color: red; display: none;"> <span > slect the unit </span> </div>
  <div class="p-size">
    <div class="p-size-text">
      <span >Weight:</span>
    </div>
    <div class="size-button">
      <select onchange = "uAmountCk()"  id = "unit" class="size-button-btn" name = "unit">
        <option value = "select">Select</option>
        <option value = "Liter"> Liter </option>
        <option value = "MiliLiter"> Mili Liter </option>
      </select> <br> 
    </div>
  </div>
  <div id = "sAlert" style = "color: red; display: none;"> <span > slect the amount </span> </div>
  <div> 
    <label style = " color : #444;" for = "unitAmount" > Amount: </label>
    <input id = "unitAmount" onchange = "uAmountCk()"  type = "number" value = "">
    </div>
  </div>`;

  if (unitGroup == "ClothSize") {
    emptydiv.innerHTML += ClothObj;
  } else if (unitGroup == "ClothPicesSize") {
    emptydiv.innerHTML += ClothPicesObj;
  } else if (unitGroup == "SolidWeight") {
    emptydiv.innerHTML += KgUnit;
  } else if (unitGroup == "LiquidWeight") {
    emptydiv.innerHTML += LiterUnit
  } else if (unitGroup == "ShoeSize") {
    emptydiv.innerHTML += ShoeSizeUnit
  }
}

var aTCBtn = document.getElementById('aTCButton')
var buyNowBTN = document.getElementById('buyNowBTN')
var buyNowa = document.getElementById('buyNowa')
var prodId = aTCBtn.getAttribute('prod')
aTCBtn.addEventListener("mouseover", uAmountCk)
buyNowBTN.addEventListener("mouseover", uAmountCk)

// This function will prevent clicking the 'add to cart' and 'buynow' button if not you select the unit or unit amount
function uAmountCk() {
  var STNAlert = document.getElementById('sAlert')
  var unitAlertElm = document.getElementById('unitAlert')

  // This try is for The product of having kg and liter unit and clothAreasize unit
  try {
    var unitAmount = document.getElementById('unitAmount').value;
    var unitType = document.getElementById("unit").value;
  } catch {
    var unitAmount = 'none';
    var unitType = "none";
  }

  if (unitAmount != 'none' && unitType != 'none') {

    if (unitType == 'select') {
      unitAlertElm.style.display = "block";
      aTCBtn.disabled = true;
      aTCBtn.style.cursor = "not-allowed";
      buyNowBTN.disabled = true;
      buyNowBTN.style.cursor = "not-allowed";
    } else {
      var attempt1 = "success"
      unitAlertElm.style.display = "none";
    }

    if (unitAmount == "" || unitAmount < 0 || unitAmount == 0) {
      STNAlert.style.display = "block";
      STNAlert.innerHTML = "select the amount"
      aTCBtn.disabled = true;
      aTCBtn.style.cursor = "not-allowed";
      buyNowBTN.disabled = true;
      buyNowBTN.style.cursor = "not-allowed";

    } else {
      var attempt2 = "success"
      STNAlert.style.display = "none";
    }

    if (attempt1 == 'success' && attempt2 == 'success') {
      MinMaxUnitCheck()
    }

  }

  //This section will work for the product having the unit of size......
  try {
    var sizeElm = document.getElementById('size').value
  } catch {
    var sizeElm = 'none';
  }

  if (sizeElm != 'none') {

    if (sizeElm == 'select') {
      unitAlertElm.style.display = "block";
      aTCBtn.disabled = true;
      aTCBtn.style.cursor = "not-allowed";
      buyNowBTN.disabled = true;
      buyNowBTN.style.cursor = "not-allowed";
    } else {
      unitAlertElm.style.display = "none"
      aTCBtn.disabled = false;
      aTCBtn.style.cursor = "pointer";
      buyNowBTN.disabled = false;
      buyNowBTN.style.cursor = "pointer";
    }
  }
  $.ajax({
    method: "GET",
    url: "/buynowdataurl",
    data: {
      unit: unitType,
      unitAmount: unitAmount,
      size: sizeElm,
      prodIdV: prodId
    },
  })
}

function MinMaxUnitCheck(){
var unit = document.getElementById('unit').value
var unitAmount = document.getElementById('unitAmount').value

$.ajax({
  method : "GET",
  url : '/mmucheckerurl',
  data : {
  prodIdV : prodId,
  unitV : unit,
  unitAmountV : unitAmount
  },
  success: function(data){
    var STNAlert = document.getElementById('sAlert')
    STNAlert.style.display = 'block'
    STNAlert.innerHTML = data.message
    if (data.attempt == true)
    {
      STNAlert.style.display = "none";
      aTCBtn.disabled = false;
      aTCBtn.style.cursor = "pointer";
      buyNowBTN.disabled = false;
      buyNowBTN.style.cursor = "pointer";
    }
    if (data.attempt == false){
      aTCBtn.disabled = true;
      aTCBtn.style.cursor = "not-allowed";
      buyNowBTN.disabled = true;
      buyNowBTN.style.cursor = "not-allowed";
    }
   
  }
})
}










// var STNAlert = document.getElementById('sAlert')
// var unitAlertElm = document.getElementById('unitAlert')
// console.log(unitAmount)
// console.log(unitType)


// if (unitAmount != "" && unitAmount > 0 && unitType != "select") {
//   aTCBtn.style.cursor = "pointer";
//   aTCBtn.disabled = false;
//   buyNowBTN.style.cursor = "pointer";
//   buyNowBTN.disabled = false;
//   STNAlert.style.display = "none";
// } 
// else
// {
//   aTCBtn.style.cursor = "not-allowed";
//   aTCBtn.disabled = true;
//   buyNowBTN.style.cursor = "not-allowed";
//   buyNowBTN.disabled = true;
//   STNAlert.style.display = "block";
// }





// This try is for The product of having kg and liter unit
// try {
//   let size = document.getElementById('size').value
//   console.log(size)
//   STNAlert = document.getElementById('sAlert')
//   if (size != 'select') {
//     aTCBtn.style.cursor = "pointer";
//     aTCBtn.disabled = false;
//     buyNowBTN.style.cursor = "pointer";
//     buyNowBTN.disabled = false;
//     STNAlert.style.display = "none";
//   } 
//   else 
//   {
//     aTCBtn.style.cursor = "not-allowed";
//     aTCBtn.disabled = true;
//     buyNowBTN.style.cursor = "not-allowed";
//     buyNowBTN.disabled = true;
//     STNAlert.style.display = "block";
//   }
//   }
// catch{}