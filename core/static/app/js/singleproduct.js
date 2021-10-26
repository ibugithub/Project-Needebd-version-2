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
  lens.onmouseover = function(){result.style.display = "block";};
  lens.onmouseout = function(){result.style.display = "none";};
  
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
    if (x > img.width - lens.offsetWidth) {x = img.width - lens.offsetWidth;}
    if (x < 0) {x = 0;}
    if (y > img.height - lens.offsetHeight) {y = img.height - lens.offsetHeight;}
    if (y < 0) {y = 0;}
    /*set the position of the lens:*/
    lens.style.left = x + "px";
    lens.style.top = y + "px";
    /*display what the lens "sees":*/
    result.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
  }
  function getCursorPos(e) {
    var a, x = 0, y = 0;
    e = e || window.event;
    /*get the x and y positions of the image:*/
    a = img.getBoundingClientRect();
    /*calculate the cursor's x and y coordinates, relative to the image:*/
    x = e.pageX - a.left;
    y = e.pageY - a.top;
    /*consider any page scrolling:*/
    x = x - window.pageXOffset;
    y = y - window.pageYOffset;
    return {x : x, y : y};
  }
};

imageZoom("myimage", "myresult");

var preview = document.getElementsByClassName('pretend_view');
var images = document.getElementById('pretend_images');
var thumbnails = document.querySelectorAll('#pretend_images > div');

thumbnails.forEach(function(elem){
  elem.onclick = onClick.bind(null, elem);
});

function onClick(elem, e){
  clearPreview();
  addToPreview(elem);
}

function clearPreview(){
  var elem = document.querySelector('.preview');
  
  if(elem){
    elem.className = elem.className.replace('preview', '');
    images.appendChild(elem);
  }
}

function addToPreview(elem){
  elem.className = 'preview';
  preview.appendChild(elem);
}

// endof zomming section



// controling the unit size etc
function addToCart(element){
  let prod_id = element.getAttribute('prod')
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
        document.getElementById('Rproduct').style.display = "none"
        document.getElementById('Sproduct').style.display = 'block'        
      }
  })
}

function fput() {
  let emptydiv = document.getElementById("EmptyDiv");
  let UnitType = emptydiv.getAttribute("unit");

  let ClothObj = ` <div class="color-size">
      <div class="p-size">
        <div class="p-size-text">
          <span >Size:</span>
        </div>
        <div class="size-button">
          <select  id = "size" class="size-button-btn" name = "unit">
            <option value = "small">Small</option>
            <option value = "medium">Medium</option>
            <option value = "large"> Large </option>
          </select>
        </div>
      </div>
    </div>`;

  let ClothPicesObj = ` <div class="color-size">
        <div class="p-size">
          <div class="p-size-text">
            <span >Unit:</span>
          </div>
          <div class="size-button">
            <select  id = "unit" class="size-button-btn" name = "unit">
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

  let KgUnit = ` <div class="color-size">
  <div class="p-size">
    <div class="p-size-text">
      <span >Weight:</span>
    </div>
    <div class="size-button">
      <select  id = "unit" class="size-button-btn" name = "unit">
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
  <div class="p-size">
    <div class="p-size-text">
      <span >Weight:</span>
    </div>
    <div class="size-button">
      <select  id = "unit" class="size-button-btn" name = "unit">
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

  let ShoeSizeUnit = ` <div class="color-size">
  <div class="p-size">
    <div class="p-size-text">
      <span >Size:</span>
    </div>
    <div class="size-button">
      <select  id = "size" class="size-button-btn" name = "unit">
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

  if (UnitType == "ClothSize") {
    emptydiv.innerHTML += ClothObj;
  } else if (UnitType == "ClothPicesSize") {
    emptydiv.innerHTML += ClothPicesObj;
  } else if (UnitType == "Kg") {
    emptydiv.innerHTML += KgUnit;
  } else if (UnitType == "Liter") {
    emptydiv.innerHTML += LiterUnit
  } else if (UnitType == "ShoeSize") {
    emptydiv.innerHTML += ShoeSizeUnit
  }

}

try{
  aTCBtn = document.getElementById('aTCButton')
aTCBtn.addEventListener("mouseover", uAmountCk)
}
catch{}

function uAmountCk() {
  try {
  unitAmount = document.getElementById('unitAmount').value
  STNAlert = document.getElementById('sAlert')
  if (unitAmount != " " && unitAmount > 0) {
    aTCBtn.style.cursor = "pointer";
    aTCBtn.disabled = false;
    STNAlert.style.display = "none"
  } else {
    aTCBtn.style.cursor = "not-allowed";
    aTCBtn.disabled = true;
    STNAlert.style.display = "block"
  }
  }
  catch{}
}