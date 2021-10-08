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
  console.log("it's connected");
  let emptydiv = document.getElementById("EmptyDiv");
  console.log("This is the emptydiv...", emptydiv);
  let UnitType = emptydiv.getAttribute("unit");
  console.log("this is UnitType...", UnitType);

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

aTCBtn = document.getElementById('aTCButton')
aTCBtn.addEventListener("mouseover", uAmountCk)

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