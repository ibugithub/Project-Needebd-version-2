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
              <option value = "Yeard"> Yeard </option>
              <option value = "Squre Meter"> Squre Meter </option>
              <option value = "Squre Yeard"> Squre Yeard </option>             
            </select>
            <label for = "unitAmount" > Amount: </label>
            <input id = "unitAmount" type = "number" value = ""  >
          </div>
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
        </select>
        <label for = "unitAmount" > Amount: </label>
        <input id = "unitAmount" type = "number" value = "">
      </div>
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
        <option value = "Mili Liter"> Mili Liter </option>
      </select>
      <label for = "unitAmount" > Amount: </label>
      <input id = "unitAmount" type = "number" value = "">
    </div>
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