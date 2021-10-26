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
