# unit amount checker....
def minMaxUnitCheckerView(request):
    request.session['buyNow_Unit_SellingCost'] = "none"
    request.session['buyNow_Total_SellingCost'] = "none"
    request.session['buyNow_Unit_DiscountedCost'] = "none"
    request.session['buyNow_Total_DiscountedCost'] = "none"
    data = {}
    productId = request.GET['prodIdV']
    fontendUnit = request.GET['unitV']
    fontendUnitAmount = float(request.GET['unitAmountV'])
    product = Product.objects.get(id = productId)
    buyNowSellingCost = product.selling_prize
    buyNowDiscountedCost = product.discounted_prize
    backendUnit = product.unit
    minUnitValue = product.MinimumUnitValue
    maxUnitValue = product.MaximumUnitValue
    backendUnitGroup = product.ProductGroup
 
    if backendUnitGroup == "SolidWeight":
        if backendUnit == "Kg":

            if fontendUnit == "Kg":
                if fontendUnitAmount >= minUnitValue and fontendUnitAmount <= maxUnitValue:
                    data["message"] = ""
                    data["attempt"] = True
                    request.session['buyNowUnit'] = fontendUnit
                    request.session['buyNowUnitAmount'] = fontendUnitAmount
                    request.session['initialUnitAmount'] = fontendUnitAmount
                    converted_Total_SellingCost = buyNowSellingCost * fontendUnitAmount
                    converted_Total_DiscountedCost = buyNowDiscountedCost * fontendUnitAmount
                    request.session['buyNow_Unit_SellingCost'] = buyNowSellingCost
                    request.session['buyNow_Total_SellingCost'] = round(converted_Total_SellingCost,2)
                    request.session['buyNow_Unit_DiscountedCost'] = buyNowDiscountedCost
                    request.session['buyNow_Total_DiscountedCost'] = round(converted_Total_DiscountedCost,2)
                                  
                else:
                    if fontendUnitAmount < minUnitValue:
                        message = f"you have to select  atleast {minUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False

                    elif fontendUnitAmount > maxUnitValue:
                        message = f"you can't select  more than {maxUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False
                            
            elif fontendUnit == "Gram":
                gramConvertedMinUnitValue = minUnitValue * 1000
                gramConvertedMaxUnitValue = maxUnitValue * 1000
                if fontendUnitAmount >= gramConvertedMinUnitValue and fontendUnitAmount <= gramConvertedMaxUnitValue:
                    data["message"] = ""
                    data["attempt"] = True
                    request.session['buyNowUnit'] = fontendUnit
                    request.session['buyNowUnitAmount'] = fontendUnitAmount
                    request.session['initialUnitAmount'] = fontendUnitAmount
                    converted_Unit_SellingCost= buyNowSellingCost * .001
                    converted_Total_SellingCost = buyNowSellingCost * .001 * fontendUnitAmount
                    converted_Unit_DiscountedCost = buyNowDiscountedCost * .001
                    converted_Total_DiscountedCost = buyNowDiscountedCost * .001 * fontendUnitAmount
                    request.session['buyNow_Unit_SellingCost'] = round(converted_Unit_SellingCost,2)
                    request.session['buyNow_Total_SellingCost'] = round(converted_Total_SellingCost,2)
                    request.session['buyNow_Unit_DiscountedCost'] = round(converted_Unit_DiscountedCost,2)
                    request.session['buyNow_Total_DiscountedCost'] = round(converted_Total_DiscountedCost, 2)
                else:
                    if fontendUnitAmount < gramConvertedMinUnitValue:
                        message = f"you have to select  atleast {gramConvertedMinUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False
                    elif fontendUnitAmount > gramConvertedMaxUnitValue:
                        message = f"you can't select  more than {gramConvertedMaxUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False

            elif fontendUnit == "Pound":
                poundConvertedMinUnitValue = round(minUnitValue * 2.20462, 2)
                poundConvertedMaxUnitValue = round(maxUnitValue * 2.20462, 2)
                if fontendUnitAmount >= poundConvertedMinUnitValue and fontendUnitAmount <= poundConvertedMaxUnitValue:                    
                    data["message"] = ""
                    data["attempt"] = True
                    request.session['buyNowUnit'] = fontendUnit
                    request.session['buyNowUnitAmount'] = fontendUnitAmount
                    request.session['initialUnitAmount'] = fontendUnitAmount
                    converted_Unit_SellingCost= buyNowSellingCost * 0.453592
                    converted_Total_SellingCost = buyNowSellingCost * 0.453592 * fontendUnitAmount
                    converted_Unit_DiscountedCost = buyNowDiscountedCost * 0.453592
                    converted_Total_DiscountedCost = buyNowDiscountedCost * 0.453592 * fontendUnitAmount
                    request.session['buyNow_Unit_SellingCost'] = round(converted_Unit_SellingCost,2)
                    request.session['buyNow_Total_SellingCost'] = round(converted_Total_SellingCost,2)
                    request.session['buyNow_Unit_DiscountedCost'] = round(converted_Unit_DiscountedCost,2)
                    request.session['buyNow_Total_DiscountedCost'] = round(converted_Total_DiscountedCost, 2)
                else:
                    if fontendUnitAmount < poundConvertedMinUnitValue:
                        message = f"you have to select  atleast {poundConvertedMinUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False
                    elif fontendUnitAmount > poundConvertedMaxUnitValue:
                        message = f"you can't select  more than {poundConvertedMaxUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False

        elif backendUnit == "Gram":
 
            if fontendUnit == "Kg":
                kgConvertedMinUnitValue = minUnitValue  *.001
                kgConvertedMaxUnitValue = maxUnitValue  *.001
                if fontendUnitAmount >= kgConvertedMinUnitValue and fontendUnitAmount <= kgConvertedMaxUnitValue:
                    data["message"] = ""
                    data["attempt"] = True
                    request.session['buyNowUnit'] = fontendUnit
                    request.session['buyNowUnitAmount'] = fontendUnitAmount
                    request.session['initialUnitAmount'] = fontendUnitAmount
                    converted_Unit_SellingCost= buyNowSellingCost * 1000
                    converted_Total_SellingCost = buyNowSellingCost * 1000 * fontendUnitAmount
                    converted_Unit_DiscountedCost = buyNowDiscountedCost * 1000
                    converted_Total_DiscountedCost = buyNowDiscountedCost * 1000 * fontendUnitAmount
                    request.session['buyNow_Unit_SellingCost'] = round(converted_Unit_SellingCost,2)
                    request.session['buyNow_Total_SellingCost'] = round(converted_Total_SellingCost,2)
                    request.session['buyNow_Unit_DiscountedCost'] = round(converted_Unit_DiscountedCost,2)
                    request.session['buyNow_Total_DiscountedCost'] = round(converted_Total_DiscountedCost, 2)
                else:  
                    if fontendUnitAmount < kgConvertedMinUnitValue:
                        message = f"you have to select  atleast {kgConvertedMinUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False
                    elif fontendUnitAmount > kgConvertedMaxUnitValue:
                        message = f"you can't select  more than {kgConvertedMaxUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False

            elif fontendUnit == "Gram":
                if fontendUnitAmount >= minUnitValue and fontendUnitAmount <= maxUnitValue:
                    data["message"] = ""
                    data["attempt"] = True
                    request.session['buyNowUnit'] = fontendUnit
                    request.session['buyNowUnitAmount'] = fontendUnitAmount
                    request.session['initialUnitAmount'] = fontendUnitAmount
                    converted_Total_SellingCost = buyNowSellingCost * fontendUnitAmount
                    converted_Total_DiscountedCost = buyNowDiscountedCost * fontendUnitAmount
                    request.session['buyNow_Unit_SellingCost'] = buyNowSellingCost
                    request.session['buyNow_Total_SellingCost'] = round(converted_Total_SellingCost,2)
                    request.session['buyNow_Unit_DiscountedCost'] = buyNowDiscountedCost
                    request.session['buyNow_Total_DiscountedCost'] = round(converted_Total_DiscountedCost,2)

                else:
                    if fontendUnitAmount < minUnitValue:
                        message = f"you have to select  atleast {minUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False
                    elif fontendUnitAmount > maxUnitValue:
                        message = f"you can't select  more than {maxUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False

            elif fontendUnit == "Pound":
                poundConvertedMinUnitValue = minUnitValue * 0.00220462
                poundConvertedMaxUnitValue = maxUnitValue * 0.00220462
                if fontendUnitAmount >=  poundConvertedMinUnitValue and fontendUnitAmount <= poundConvertedMaxUnitValue:
                    data["message"] = ""
                    data["attempt"] = True
                    request.session['buyNowUnit'] = fontendUnit
                    request.session['buyNowUnitAmount'] = fontendUnitAmount
                    request.session['initialUnitAmount'] = fontendUnitAmount
                    converted_Unit_SellingCost= buyNowSellingCost * 453.592
                    converted_Total_SellingCost = buyNowSellingCost * 453.592 * fontendUnitAmount
                    converted_Unit_DiscountedCost = buyNowDiscountedCost * 453.592
                    converted_Total_DiscountedCost = buyNowDiscountedCost * 453.592 * fontendUnitAmount
                    request.session['buyNow_Unit_SellingCost'] = round(converted_Unit_SellingCost,2)
                    request.session['buyNow_Total_SellingCost'] = round(converted_Total_SellingCost,2)
                    request.session['buyNow_Unit_DiscountedCost'] = round(converted_Unit_DiscountedCost,2)
                    request.session['buyNow_Total_DiscountedCost'] = round(converted_Total_DiscountedCost, 2)
                else:
                    if fontendUnitAmount < poundConvertedMinUnitValue:
                        message = f"you have to select  atleast {poundConvertedMinUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False
                    elif fontendUnitAmount > poundConvertedMaxUnitValue:
                        message = f"you can't select  more than {poundConvertedMaxUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False

        elif backendUnit == "Pound":
            if fontendUnit == "Kg":
                kgConvertedMinUnitValue = minUnitValue * 0.453592
                kgConvertedMaxUnitValue = maxUnitValue * 0.453592
                if fontendUnitAmount >= kgConvertedMinUnitValue and fontendUnitAmount <= kgConvertedMaxUnitValue:
                    data["message"] = ""
                    data["attempt"] = True
                    request.session['buyNowUnit'] = fontendUnit
                    request.session['buyNowUnitAmount'] = fontendUnitAmount
                    request.session['initialUnitAmount'] = fontendUnitAmount
                    converted_Unit_SellingCost= buyNowSellingCost * 2.20462
                    converted_Total_SellingCost = buyNowSellingCost * 2.20462 * fontendUnitAmount
                    converted_Unit_DiscountedCost = buyNowDiscountedCost * 2.20462
                    converted_Total_DiscountedCost = buyNowDiscountedCost * 2.20462 * fontendUnitAmount
                    request.session['buyNow_Unit_SellingCost'] = round(converted_Unit_SellingCost,2)
                    request.session['buyNow_Total_SellingCost'] = round(converted_Total_SellingCost,2)
                    request.session['buyNow_Unit_DiscountedCost'] = round(converted_Unit_DiscountedCost,2)
                    request.session['buyNow_Total_DiscountedCost'] = round(converted_Total_DiscountedCost, 2)
                else:
                    if fontendUnitAmount < kgConvertedMinUnitValue:
                        message = f"you have to select  atleast {kgConvertedMinUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False
                    elif fontendUnitAmount > kgConvertedMaxUnitValue:
                        message = f"you can't select  more than {kgConvertedMaxUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False

            elif fontendUnit == "Gram":
                gramConvertedMinUnitValue = minUnitValue * 453.592
                gramConvertedMaxUnitValue = maxUnitValue * 453.592
                if fontendUnitAmount >= gramConvertedMinUnitValue and fontendUnitAmount <= gramConvertedMaxUnitValue:
                    data["message"] = ""
                    data["attempt"] = True
                    request.session['buyNowUnit'] = fontendUnit
                    request.session['buyNowUnitAmount'] = fontendUnitAmount
                    request.session['initialUnitAmount'] = fontendUnitAmount
                    converted_Unit_SellingCost= buyNowSellingCost * 0.00220462
                    converted_Total_SellingCost = buyNowSellingCost * 0.00220462 * fontendUnitAmount
                    converted_Unit_DiscountedCost = buyNowDiscountedCost * 0.00220462
                    converted_Total_DiscountedCost = buyNowDiscountedCost * 0.00220462 * fontendUnitAmount
                    request.session['buyNow_Unit_SellingCost'] = round(converted_Unit_SellingCost,2)
                    request.session['buyNow_Total_SellingCost'] = round(converted_Total_SellingCost,2)
                    request.session['buyNow_Unit_DiscountedCost'] = round(converted_Unit_DiscountedCost,2)
                    request.session['buyNow_Total_DiscountedCost'] = round(converted_Total_DiscountedCost, 2)
                    
                else:
                    if fontendUnitAmount < gramConvertedMinUnitValue:
                        message = f"you have to select  atleast {gramConvertedMinUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False
                    elif fontendUnitAmount > gramConvertedMaxUnitValue:
                        message = f"you can't select  more than {gramConvertedMaxUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False

            elif fontendUnit == "Pound":
                if fontendUnitAmount >= minUnitValue and fontendUnitAmount <= maxUnitValue:
                    data["message"] = ""
                    data["attempt"] = True
                    request.session['buyNowUnit'] = fontendUnit
                    request.session['buyNowUnitAmount'] = fontendUnitAmount
                    request.session['initialUnitAmount'] = fontendUnitAmount
                    converted_Total_SellingCost = buyNowSellingCost * fontendUnitAmount
                    converted_Total_DiscountedCost = buyNowDiscountedCost * fontendUnitAmount
                    request.session['buyNow_Unit_SellingCost'] = buyNowSellingCost
                    request.session['buyNow_Total_SellingCost'] = round(converted_Total_SellingCost,2)
                    request.session['buyNow_Unit_DiscountedCost'] = buyNowDiscountedCost
                    request.session['buyNow_Total_DiscountedCost'] = round(converted_Total_DiscountedCost,2)
                else:
                    if fontendUnitAmount < minUnitValue:
                        message = f"you have to select  atleast {minUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False
                    elif fontendUnitAmount > maxUnitValue:
                        message = f"you can't select  more than {maxUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False

    if backendUnitGroup == "LiquidWeight":

        if backendUnit == "Liter":
            if fontendUnit == "Liter":
                if fontendUnitAmount >= minUnitValue and fontendUnitAmount <= maxUnitValue:
                    data["message"] = ""
                    data["attempt"] = True
                    request.session['buyNowUnit'] = fontendUnit
                    request.session['buyNowUnitAmount'] = fontendUnitAmount
                    request.session['initialUnitAmount'] = fontendUnitAmount
                    converted_Total_SellingCost = buyNowSellingCost * fontendUnitAmount
                    converted_Total_DiscountedCost = buyNowDiscountedCost * fontendUnitAmount
                    request.session['buyNow_Unit_SellingCost'] = buyNowSellingCost
                    request.session['buyNow_Total_SellingCost'] = round(converted_Total_SellingCost,2)
                    request.session['buyNow_Unit_DiscountedCost'] = buyNowDiscountedCost
                    request.session['buyNow_Total_DiscountedCost'] = round(converted_Total_DiscountedCost,2)
                   
                else:
                    if fontendUnitAmount < minUnitValue:
                        message = f"you have to select  atleast {minUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False
                    elif fontendUnitAmount > maxUnitValue:
                        message = f"you can't select  more than {maxUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False

            elif fontendUnit == "MiliLiter":
                MLConvertedMinUnitValue = minUnitValue * 1000
                MLConvertedMaxUnitValue = maxUnitValue * 1000
                if fontendUnitAmount >= MLConvertedMinUnitValue and fontendUnitAmount <= MLConvertedMaxUnitValue:
                    data["message"] = ""
                    data["attempt"] = True
                    request.session['buyNowUnit'] = fontendUnit
                    request.session['buyNowUnitAmount'] = fontendUnitAmount
                    request.session['initialUnitAmount'] = fontendUnitAmount
                    converted_Unit_SellingCost= buyNowSellingCost * 0.001
                    converted_Total_SellingCost = buyNowSellingCost * 0.001 * fontendUnitAmount
                    converted_Unit_DiscountedCost = buyNowDiscountedCost * 0.001
                    converted_Total_DiscountedCost = buyNowDiscountedCost * 0.001 * fontendUnitAmount
                    request.session['buyNow_Unit_SellingCost'] = round(converted_Unit_SellingCost,2)
                    request.session['buyNow_Total_SellingCost'] = round(converted_Total_SellingCost,2)
                    request.session['buyNow_Unit_DiscountedCost'] = round(converted_Unit_DiscountedCost,2)
                    request.session['buyNow_Total_DiscountedCost'] = round(converted_Total_DiscountedCost, 2)

                else:
                    if fontendUnitAmount < MLConvertedMinUnitValue:
                        message = f"you have to select  atleast {MLConvertedMinUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False
                    elif fontendUnitAmount > MLConvertedMaxUnitValue:
                        message = f"you can't select  more than {MLConvertedMaxUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False

        elif backendUnit == "MiliLiter":
            if fontendUnit == "Liter":
                LiterConvertedMinUnitVAlue = minUnitValue * 0.001
                LiterConvertedMaxUnitVAlue = maxUnitValue * 0.001
                if fontendUnitAmount >= LiterConvertedMinUnitVAlue and fontendUnitAmount <= LiterConvertedMaxUnitVAlue:
                    data["message"] = ""
                    data["attempt"] = True
                    request.session['buyNowUnit'] = fontendUnit
                    request.session['buyNowUnitAmount'] = fontendUnitAmount
                    request.session['initialUnitAmount'] = fontendUnitAmount
                    converted_Unit_SellingCost= buyNowSellingCost * 1000
                    converted_Total_SellingCost = buyNowSellingCost * 1000 * fontendUnitAmount
                    converted_Unit_DiscountedCost = buyNowDiscountedCost * 1000
                    converted_Total_DiscountedCost = buyNowDiscountedCost * 1000 * fontendUnitAmount
                    request.session['buyNow_Unit_SellingCost'] = round(converted_Unit_SellingCost,2)
                    request.session['buyNow_Total_SellingCost'] = round(converted_Total_SellingCost,2)
                    request.session['buyNow_Unit_DiscountedCost'] = round(converted_Unit_DiscountedCost,2)
                    request.session['buyNow_Total_DiscountedCost'] = round(converted_Total_DiscountedCost, 2)

                else:
                    if fontendUnitAmount < LiterConvertedMinUnitVAlue:
                        message = f"you have to select  atleast {LiterConvertedMinUnitVAlue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False
                    elif fontendUnitAmount > LiterConvertedMaxUnitVAlue:
                        message = f"you can't select  more than {LiterConvertedMaxUnitVAlue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False

            elif fontendUnit == "MiliLiter":
                if fontendUnitAmount >= minUnitValue and fontendUnitAmount <= maxUnitValue:
                    data["message"] = ""
                    data["attempt"] = True
                    request.session['buyNowUnit'] = fontendUnit
                    request.session['buyNowUnitAmount'] = fontendUnitAmount
                    request.session['initialUnitAmount'] = fontendUnitAmount
                    converted_Total_SellingCost = buyNowSellingCost * fontendUnitAmount
                    converted_Total_DiscountedCost = buyNowDiscountedCost * fontendUnitAmount
                    request.session['buyNow_Unit_SellingCost'] = buyNowSellingCost
                    request.session['buyNow_Total_SellingCost'] = round(converted_Total_SellingCost,2)
                    request.session['buyNow_Unit_DiscountedCost'] = buyNowDiscountedCost
                    request.session['buyNow_Total_DiscountedCost'] = round(converted_Total_DiscountedCost,2)

                else:
                    if fontendUnitAmount < minUnitValue:
                        message = f"you have to select  atleast {minUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False
                    elif fontendUnitAmount > maxUnitValue:
                        message = f"you can't select  more than {maxUnitValue} {fontendUnit} for this product"
                        data["message"] = message
                        data["attempt"] = False

    return JsonResponse(data)

# unitAmount in plus and minus....
def Buynow(request, pk = None):
    request.session['buyNowSubTotal'] = 'none'
    request.session['buyNowTotal'] = 'none'
    request.session['buyNowDiscount'] = 'none'
    request.session['buyNowQuantity'] = "none"
    context = {}

    try:
        defaultAddress = CustomerAddress.objects.get(user = request.user, isDefault = True)
    except:
        return redirect('/aaddressurl')
    newProfile = CustomerProfile.objects.get(user = request.user)
    newAddress = CustomerAddress.objects.filter(user = request.user)
    if  len(newAddress) < 1:
            return redirect('/abookurl')    
    context['newaddress'] = newAddress
    context["daddress"] = defaultAddress
    context["profile"] = newProfile
    
     # initial product info will be shown by this section
    if pk != None:
        # This section will work for packet product.............
        request.session['buyNowProdId'] = pk
        newProduct = Product.objects.get(id = pk)
        subTotal = newProduct.discounted_prize
        shippingCost = 70
        total = subTotal + shippingCost
        context["product"] = newProduct
        context['subtotal'] = subTotal
        context["shippingCost"] = shippingCost
        context["total"] = total
        request.session['buyNowSubTotal'] = subTotal
        request.session['buyNowTotal'] = total
        request.session['buyNowQuantity'] = 1

        # This section will only work on when product will have unit Type of solid weight or Liquid weight
        if newProduct.ProductGroup == "SolidWeight" or newProduct.ProductGroup == "LiquidWeight":
            context['buyNowUnit'] = request.session['buyNowUnit']
            context['buyNowUnitAmount'] = request.session['buyNowUnitAmount']
            context['Unit_SellingCost'] = request.session['buyNow_Unit_SellingCost']
            context['Total_SellingCost'] = request.session['buyNow_Total_SellingCost']
            context['Unit_DiscountedCost'] = request.session['buyNow_Unit_DiscountedCost']
            context["Total_DiscountedCost"] = request.session['buyNow_Total_DiscountedCost']
            subTotal2 = request.session['buyNow_Total_DiscountedCost']
            Total2 = subTotal2 + shippingCost
            context['subtotal'] = subTotal2
            context['total'] = Total2
            request.session['buyNowSubTotal'] = subTotal2
            request.session['buyNowTotal'] = Total2
       
        return render(request, 'app/buyNowCheckout.html',context = context)

    # plus and minus action in buy now page will work on this section when product having packet ProductGroup...    
    if pk == None:
        Group = request.GET['Group']
        if Group == "packet":
            productId = request.GET['productId']
            quantity = int(request.GET['quantity'])
            request.session['buyNowQuantity'] = quantity
            newProduct = Product.objects.get(id = productId)
            shippingCost = 70      
            subTotal = newProduct.discounted_prize * quantity
            total = subTotal + shippingCost
            request.session['buyNowSubTotal'] = subTotal
            request.session["buyNowTotal"] = total
            data = {
                'subTotal': subTotal,
                "total" : total
            }

        # plus and minus action in buy now page will work on this section when product having solid and Liquid weight ProductGroup...  
        elif Group == "nonpacket":
            data = {}
            action = request.GET['action']
            prouductId = request.GET['productId']
            newProduct = Product.objects.get(id = prouductId)
            initialUnitAmount = request.session['initialUnitAmount']
            unitAmount = float(request.session['buyNowUnitAmount'])
            unitSellingCost = request.session['buyNow_Unit_SellingCost']
            unitDiscountedCost = request.session['buyNow_Unit_DiscountedCost']
            unit = newProduct.unit
            userSelectedUnit = request.session['buyNowUnit']
            unitFrequency = newProduct.unitValue_On_Increase_or_Decrease
            minUnitValue = newProduct.MinimumUnitValue
            maxUnitValue = newProduct.MaximumUnitValue

            if newProduct.ProductGroup == "SolidWeight":
                if unit == "Kg":
                    
                    if userSelectedUnit == "Kg":
                        diff = round((initialUnitAmount/minUnitValue) - minUnitValue, 2)
                        diff2 = round((initialUnitAmount/minUnitValue) - diff, 2)
                        if action == "plus":
                            if not unitAmount >= maxUnitValue:
                                unitAmount += unitFrequency
                        if action == "minus":
                            if not unitAmount - diff2 <= minUnitValue:
                                unitAmount -= unitFrequency
                            else:
                                unitAmount -= (unitAmount - diff2)


                    if  userSelectedUnit == "Gram":
                        cUnitFrequency = round(unitFrequency * 1000, 2)
                        minUnitValue = round(minUnitValue * 1000, 2)
                        maxUnitValue = round(maxUnitValue * 1000, 2)
                        diff = round((initialUnitAmount/minUnitValue) - minUnitValue, 2)
                        diff2 = round((initialUnitAmount/minUnitValue) - diff, 2)
                        if action == "plus":
                            if not unitAmount >= maxUnitValue:
                                unitAmount += cUnitFrequency
                        if action == "minus":
                            if not unitAmount-diff2 <= minUnitValue:
                                unitAmount -= cUnitFrequency
                            else:
                                unitAmount -= (unitAmount - diff2)

                    
                    if  userSelectedUnit == "Pound":
                        cUnitFrequency = round(unitFrequency * 2.20462, 2)
                        minUnitValue = round(minUnitValue * 2.20462, 2)
                        maxUnitValue = round(maxUnitValue * 2.20462, 2)
                        diff = round((initialUnitAmount/minUnitValue) - minUnitValue ,2)
                        diff2 = round((initialUnitAmount/minUnitValue) - diff ,2)
                        if action == "plus":
                            if not unitAmount >= maxUnitValue:
                                unitAmount += cUnitFrequency
                        if action == "minus":
                            if not unitAmount - diff2 <= minUnitValue:
                                unitAmount -= cUnitFrequency
                            else:
                                unitAmount -= (unitAmount - diff2)
                                                       
                if unit == "Gram":
                    if userSelectedUnit == "Gram":
                        diff = round((initialUnitAmount/minUnitValue) - minUnitValue, 2)
                        diff2 = round((initialUnitAmount/minUnitValue) - diff, 2)
                        if action == "plus":
                            if not unitAmount >= maxUnitValue:
                                unitAmount += unitFrequency
                        if action == "minus":
                            if not unitAmount - diff2 <= minUnitValue:
                                unitAmount -= unitFrequency
                            else:
                                unitAmount -= (unitAmount - diff2)
                                               
                    if userSelectedUnit == "Kg":
                        cUnitFrequency = round(unitFrequency * .001, 2)
                        minUnitValue = round(minUnitValue * .001, 2)
                        maxUnitValue = round(maxUnitValue * .001, 2)
                        diff = round((initialUnitAmount/minUnitValue) - minUnitValue, 2)
                        diff2 = round((initialUnitAmount/minUnitValue) - diff, 2)
                        if action == "plus":
                            if not unitAmount >= maxUnitValue:
                                unitAmount += cUnitFrequency
                        if action == "minus":
                            if not unitAmount-diff2 <= minUnitValue:
                                unitAmount -= cUnitFrequency
                            else:
                                unitAmount -= (unitAmount - diff2)
                    
                    if userSelectedUnit == "Pound":
                        cUnitFrequency = round(unitFrequency * 0.00220462, 2)
                        minUnitValue = round(minUnitValue * 0.00220462, 2)
                        maxUnitValue = round(maxUnitValue * 0.00220462, 2)
                        diff = round((initialUnitAmount/minUnitValue) - minUnitValue, 2)
                        diff2 = round((initialUnitAmount/minUnitValue) - diff, 2)
                        if action == "plus":
                            if not unitAmount >= maxUnitValue:
                                unitAmount += cUnitFrequency
                        if action == "minus":
                            if not unitAmount-diff2 <= minUnitValue:
                                unitAmount -= cUnitFrequency
                            else:
                                unitAmount -= (unitAmount - diff2)

                if unit == "Pound":
                    if userSelectedUnit == "Pound":

                        diff = round((initialUnitAmount/minUnitValue) - minUnitValue, 2)
                        diff2 = round((initialUnitAmount/minUnitValue) - diff, 2)
                        if action == "plus":
                            if not unitAmount >= maxUnitValue:
                                unitAmount += unitFrequency
                        if action == "minus":
                            if not unitAmount - diff2 <= minUnitValue:
                                unitAmount -= unitFrequency
                            else:
                                unitAmount -= (unitAmount - diff2)
                        
                    if userSelectedUnit == "Kg":

                        cUnitFrequency = round(unitFrequency * 0.453592, 2)
                        minUnitValue = round(minUnitValue * 0.453592, 2)
                        maxUnitValue = round(maxUnitValue * 0.453592, 2)
                        diff = round((initialUnitAmount/minUnitValue) - minUnitValue, 2)
                        diff2 = round((initialUnitAmount/minUnitValue) - diff, 2)
                        if action == "plus":
                            if not unitAmount >= maxUnitValue:
                                unitAmount += cUnitFrequency
                        if action == "minus":
                            if not unitAmount-diff2 <= minUnitValue:
                                unitAmount -= cUnitFrequency
                            else:
                                unitAmount -= (unitAmount - diff2)
                        
                    if userSelectedUnit == "Gram":

                        cUnitFrequency = round(unitFrequency * 453.592, 2)
                        minUnitValue = round(minUnitValue * 453.592, 2)
                        maxUnitValue = round(maxUnitValue * 453.592, 2)
                        diff = round((initialUnitAmount/minUnitValue) - minUnitValue, 2)
                        diff2 = round((initialUnitAmount/minUnitValue) - diff, 2)
                        if action == "plus":
                            if not unitAmount >= maxUnitValue:
                                unitAmount += cUnitFrequency
                        if action == "minus":
                            if not unitAmount-diff2 <= minUnitValue:
                                unitAmount -= cUnitFrequency
                            else:
                                unitAmount -= (unitAmount - diff2)
                                
            if newProduct.ProductGroup == "LiquidWeight":
                if unit == "Liter":
                    if userSelectedUnit  == "Liter":
                        diff = round((initialUnitAmount/minUnitValue) - minUnitValue, 2)
                        diff2 = round((initialUnitAmount/minUnitValue) - diff, 2)
                        if action == "plus":
                            if not unitAmount >= maxUnitValue:
                                unitAmount += unitFrequency
                        if action == "minus":
                            if not unitAmount - diff2 <= minUnitValue:
                                unitAmount -= unitFrequency
                            else:
                                unitAmount -= (unitAmount - diff2)

                    if userSelectedUnit == "MiliLiter":
                        cUnitFrequency = round(unitFrequency * 1000, 2)
                        minUnitValue = round(minUnitValue * 1000, 2)
                        maxUnitValue = round(maxUnitValue * 1000, 2)
                        diff = round((initialUnitAmount/minUnitValue) - minUnitValue, 2)
                        diff2 = round((initialUnitAmount/minUnitValue) - diff, 2)
                        if action == "plus":
                            if not unitAmount >= maxUnitValue:
                                unitAmount += cUnitFrequency
                        if action == "minus":
                            if not unitAmount-diff2 <= minUnitValue:
                                unitAmount -= cUnitFrequency
                            else:
                                unitAmount -= (unitAmount - diff2)

                if unit == "MiliLiter":
                    if userSelectedUnit == "MiliLiter":
                        diff = round((initialUnitAmount/minUnitValue) - minUnitValue, 2)
                        diff2 = round((initialUnitAmount/minUnitValue) - diff, 2)
                        if action == "plus":
                            if not unitAmount >= maxUnitValue:
                                unitAmount += unitFrequency
                        if action == "minus":
                            if not unitAmount - diff2 <= minUnitValue:
                                unitAmount -= unitFrequency
                            else:
                                unitAmount -= (unitAmount - diff2)

                    if userSelectedUnit == "Liter":
                        cUnitFrequency = round(unitFrequency * .001, 2)
                        minUnitValue = round(minUnitValue * .001, 2)
                        maxUnitValue = round(maxUnitValue * .001, 2)
                        diff = round((initialUnitAmount/minUnitValue) - minUnitValue, 2)
                        diff2 = round((initialUnitAmount/minUnitValue) - diff, 2)
                        if action == "plus":
                            if not unitAmount >= maxUnitValue:
                                unitAmount += cUnitFrequency
                        if action == "minus":
                            if not unitAmount-diff2 <= minUnitValue:
                                unitAmount -= cUnitFrequency
                            else:
                                unitAmount -= (unitAmount - diff2)
            
            data['unitAmount'] = round(unitAmount, 2)    
            request.session['buyNowUnitAmount'] = unitAmount
            sellingCost = round(unitSellingCost * unitAmount, 2)
            discountedCost = round(unitDiscountedCost * unitAmount, 2)
            data['sellingCost'] = sellingCost
            data['discountedCost'] = discountedCost
            request.session['buyNow_Total_SellingCost'] = sellingCost
            request.session['buyNow_Total_DiscountedCost'] = discountedCost
            shippingCost = 70
            total = discountedCost + shippingCost
            data['total'] = total
            request.session['buyNowSubTotal'] = discountedCost
            request.session['buyNowTotal'] = total
        return JsonResponse(data)
