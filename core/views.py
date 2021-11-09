from datetime import timedelta
import datetime
import json
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.detail import DetailView
from .models import (Brand_Logo_row1, Brand_Logo_row2, Brand_Logo_row3,
                     Category, Slider, Mobile_Category, Footer_Colum1,
                     Footer_Colum2, Footer_Colum3, Footer_Colum4, Product,
                     CategoryWraper, Cart, CustomerProfile, Divisions,
                     Districts, Unions, Upazilas, CustomerAddress, Order)
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, TemplateView, View
from django.http import JsonResponse
from coupons.models import Coupon, Voucher
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator


# Create your views here.
class Mycontext(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['footer_colum_1'] = Footer_Colum1.objects.all()
        context['footer_colum_2'] = Footer_Colum2.objects.all()
        context['footer_colum_3'] = Footer_Colum3.objects.all()
        context['footer_colum_4'] = Footer_Colum4.objects.all()
        if self.request.user.is_authenticated:
            carts = Cart.objects.filter(user=self.request.user)
            context['item'] = len(carts)
        return context

class IndexView(Mycontext, ListView):
    model = Category
    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uppercategories'] = CategoryWraper.objects.filter(
            display_wraper__name='Upper_Category')
        context['bookandstudy'] = Category.objects.filter(
            category_wraper__name='Books & Study')
        context['cookingessential'] = Category.objects.filter(
            category_wraper__name='Cooking Essential')
        context['electronic'] = Category.objects.filter(
            category_wraper__name='Electronic')
        context['girlsandkids'] = Category.objects.filter(
            category_wraper__name='Girls & Kids')
        context['homeessential'] = Category.objects.filter(
            category_wraper__name='Home Essential')
        context['msliders'] = Slider.objects.filter(device='Mobile')
        context['fashion'] = Category.objects.filter(
            category_wraper__name='Fashion')
        context['handmade'] = Category.objects.filter(
            category_wraper__name='Handmade')
        context['other'] = Category.objects.filter(
            category_wraper__name='Other')
        context['dsliders'] = Slider.objects.filter(device='Desktop')
        context['brand_logo_row1'] = Brand_Logo_row1.objects.all()
        context['brand_logo_row2'] = Brand_Logo_row2.objects.all()
        context['brand_logo_row3'] = Brand_Logo_row3.objects.all()
        context['mobile_category'] = Mobile_Category.objects.all()
        context['shop_with_deals'] = Product.objects.filter(
            display_wraper__name='Shop With Deal')
        context['beauty_products'] = Product.objects.filter(
            display_wraper__name='Beauty Product')
        context['mans_fashions'] = Product.objects.filter(
            display_wraper__name='Mans Fashion')

        return context

def account(request):
    return render(request, 'app/account.html')

class AllCategoryView(Mycontext, ListView):
    model = Footer_Colum1
    template_name = 'app/allcategories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_wrapers_upper'] = CategoryWraper.objects.all()[:6]
        context['category_wraper_upper2'] = CategoryWraper.objects.all()[7:12]
        context['category_wraper_all'] = CategoryWraper.objects.all()
        context['category'] = Category.objects.all()
        return context

class ProductPageView(Mycontext, ListView):
    model = Product
    paginate_by = 10
    context_object_name = 'products'
    template_name = 'app/ProductPage.html'

    def get_queryset(self):
        qs = super(ProductPageView, self).get_queryset()
        return qs.filter(product_category__title=self.kwargs.get('category'))

def SingleProductView(request, pk): 
    template_name = 'app/singleproduct.html'
    product = Product.objects.get(id = pk)
    category = product.product_category
    relatedProduct = Product.objects.filter(product_category = category)
    paginator = Paginator(relatedProduct, 11)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "product" : product,
        "relatedProduct" : relatedProduct,
        "showedProductId" : pk,
        "page_obj" : page_obj
    }
    return render(request, template_name, context = context)
    
def AddToCartView(request):
    product_id = request.GET['productid']
    unit = request.GET['unit']
    unit_amount = request.GET['unit_amount']
    size = request.GET['Size']
    if request.user.is_authenticated:
        user = request.user
        myproduct = Product.objects.get(id=product_id)

        # Carting the product info for the prduct having KG unit or Liter Unit
        if myproduct.unitGroup == "SolidWeight" or myproduct.unitGroup == "LiquidWeight" or myproduct.unitGroup == "ClothPicesSize":
            try:
                cart = Cart.objects.get(user=user,
                                        product=myproduct,
                                        unitGroup=unit,
                                        unit_amount = unit_amount
                                        )
                cart.unit_amount += 1
                cart.save()
            except:
                Cart(user=user,
                     product=myproduct,
                     unit=unit,
                     unit_amount=unit_amount).save()
        elif myproduct.unitGroup == "ClothSize" or myproduct.unitGroup == "ShoeSize":
            try:
                cart = Cart.objects.get(user=user,
                                        product=myproduct,
                                        size=size)
                cart.quantity += 1
                cart.save()
            except:
                Cart(user=user, product=myproduct, size=size).save()
        elif myproduct.unitGroup == "Packet":
            try:
                cart = Cart.objects.get(user=user, product=myproduct)
                cart.quantity += 1
                cart.save()
            except:
                Cart(user=user, product=myproduct).save()
    data = {'demo': "data"}
    return JsonResponse(data)

class ShowCartView(TemplateView):
    template_name = 'app/CartPage.html'

    def get(self, request, *args, **kwargs):
        request.session['code'] = 'none'
        if request.user.is_authenticated:
            user = request.user
            carts = Cart.objects.filter(user=user)

            Total_Selling_Cost = 0
            Total_products_cost = 0
            Total_discount = 0
            Item = 0
            for cart in carts:
                Total_Selling_Cost += cart.products_total_selling_cost
                Total_products_cost += cart.products_total_cost
                Total_discount += (cart.products_total_selling_cost -
                                   cart.products_total_cost)
                Item += 1
            delivery_cost = 70
            Total_Cost = Total_products_cost + delivery_cost

            if Total_Cost == delivery_cost:
                Total_Cost = 0
            return render(
                request, self.template_name, {
                    'carts': carts,
                    "Total_Cost": Total_Cost,
                    "Item": Item,
                    "Total_Selling_Cost": Total_Selling_Cost,
                    "Total_discount": Total_discount,
                    "delivery_cost": delivery_cost,
                })
        else:
            return redirect('/accounts/login/')

def PlusCartView(request):
    request.session['code'] = 'none'
    if request.user.is_authenticated:
        user = request.user
        product_key = request.GET['id']
        product = Product.objects.get(id=product_key)
        unit = request.GET['unit']
        unit_amount = request.GET['unit_amount']
        size = request.GET['size']

        if product.unitGroup == "SolidWeight" or product.unitGroup == "LiquidWeight" or product.unitGroup == "ClothPicesSize":
            cart = Cart.objects.get(user=user,
                                    product=product,
                                    unit=unit,
                                    unit_amount=unit_amount)
            cart.quantity += 1
            cart.save()
        elif product.unitGroup == "ClothSize" or product.unitGroup == "ShoeSize":
            cart = Cart.objects.get(user=user, product=product, size=size)
            cart.quantity += 1
            cart.save()
        elif product.unitGroup == "Packet":
            cart = Cart.objects.get(user=user, product=product)
            cart.quantity += 1
            cart.save()

        carts = Cart.objects.filter(user=user)
        TotalSell_Cost = 0
        Total_products_cost = 0
        Total_discount = 0
        for tccart in carts:
            TotalSell_Cost += tccart.products_total_selling_cost
            Total_products_cost += tccart.products_total_cost
            Total_discount += (tccart.products_total_selling_cost -
                               tccart.products_total_cost)
        delivery_charge = 70
        Total_Cost = Total_products_cost + delivery_charge

        data = {
            'quantity': cart.quantity,
            "TotalSell_Cost": TotalSell_Cost,
            'products_total_cost': cart.products_total_cost,
            'Total_Cost': Total_Cost,
            'Total_discount': Total_discount
        }
        return JsonResponse(data)

def MinusCartView(request):
    request.session['code'] = 'none'
    user = request.user
    if user.is_authenticated:
        product_key = request.GET['id']
        product = Product.objects.get(id=product_key)
        unit = request.GET['unit']
        unit_amount = request.GET['unit_amount']
        size = request.GET['size']

        def itemcount():
            Item = 0
            icarts = Cart.objects.filter(user=user)
            for icart in icarts:
                Item += 1
            return Item

        if product.unitGroup == "LiquidWeight" or product.unitGroup == "SolidWeight" or product.unitGroup == "ClothPicesSize":
            cart = Cart.objects.get(user=user,
                                    product=product,
                                    unit=unit,
                                    unit_amount=unit_amount)
            if cart.quantity >= 1:
                cart.quantity -= 1
                cart.save()
            if cart.quantity == 0:
                cart.delete()
                Item = itemcount()
        elif product.unitGroup == "ClothSize" or product.unitGroup == "ShoeSize":
            cart = Cart.objects.get(user=user, product=product, size=size)
            if cart.quantity >= 1:
                cart.quantity -= 1
                cart.save()
            if cart.quantity <= 0:
                cart.delete()
                Item = itemcount()
        elif product.unitGroup == "Packet":
            cart = Cart.objects.get(user=user, product=product)
            if cart.quantity >= 1:
                cart.quantity -= 1
                cart.save()
            if cart.quantity <= 0:
                cart.delete()
                Item = itemcount()

        newcart = Cart.objects.filter(user=user)
        cartCount = len(newcart)
        if cartCount <= 0:
            cartCount = 0
        TotalSell_Cost = 0
        Total_products_cost = 0
        Total_discount = 0
        delivery_cost = 70
        for tccart in newcart:
            TotalSell_Cost += tccart.products_total_selling_cost
            Total_products_cost += tccart.products_total_cost
            Total_discount += (tccart.products_total_selling_cost -
                               tccart.products_total_cost)
        Total_Cost = Total_products_cost + delivery_cost
        if Total_Cost == delivery_cost:
            Total_Cost = 0
        try:
            Item
        except:
            Item = 0
            for icart in newcart:
                Item += 1

        data = {
            'quantity': cart.quantity,
            "TotalSell_Cost": TotalSell_Cost,
            'products_total_cost': cart.products_total_cost,
            'cartCount': cartCount,
            "Total_Cost": Total_Cost,
            "Item": Item,
            "Total_discount": Total_discount
        }
        return JsonResponse(data)

def RemoveCartView(request):
    request.session['code'] = 'none'
    user = request.user
    product_key = request.GET['prod_id']
    product = Product.objects.get(id=product_key)
    unit = request.GET['unit']
    unit_amount = request.GET['unit_amount']
    size = request.GET['size']
    if product.unitGroup == "LiquidWeight" or product.unitGroup == "SolidWeight" or product.unitGroup == "ClothPicesSize":
        cart = Cart.objects.get(user=user,
                                product=product,
                                unit=unit,
                                unit_amount=unit_amount)
        cart.delete()

    elif product.unitGroup== "ClothSize" or product.unitGroup == "ShoeSize":
        cart = Cart.objects.get(user=user, product=product, size=size)
        cart.delete()

    elif product.unitGroup== "Packet":
        cart = Cart.objects.get(user=user, product=product)
        cart.delete()

    cart = Cart.objects.filter(user=request.user)
    cartCount = len(cart)
    if cartCount <= 0:
        cartCount = 0
    TotalSell_Cost = 0
    Total_products_cost = 0
    delivery_cost = 70
    Total_discount = 0
    Item = 0
    for tccart in cart:
        TotalSell_Cost += tccart.products_total_selling_cost
        Total_products_cost += tccart.products_total_cost
        Total_discount += (tccart.products_total_selling_cost -
                           tccart.products_total_cost)
        Item += 1
    Total_Cost = Total_products_cost + delivery_cost
    if Total_Cost == delivery_cost:
        Total_Cost = 0

    data = {
        'cartCount': cartCount,
        "TotalSell_Cost": TotalSell_Cost,
        "Total_Cost": Total_Cost,
        "Total_discount": Total_discount,
        "Item": Item
    }
    return JsonResponse(data)

def VoucherChecker(request, redirect = False):
    carts = Cart.objects.filter(user=request.user)
    total_amount = 0
    for cart in carts:
        total_amount += cart.products_total_cost
    delivery_cost = 70

    if redirect == True:
        code = request.session['code']
    else:
        code = request.GET['code']
    
    now = timezone.now()
    try:
        coupon = Coupon.objects.get(coupon_code=code,
                                    valid_from__lte=now,
                                    valid_to__gte=now,
                                    active=True)
        discount = coupon.discount
        if not coupon.condition_rate == None:
            if total_amount >= coupon.condition_rate:
                message = ""
                total_amount = (total_amount - coupon.discount) + delivery_cost
                request.session['code'] = code
            else:
                message = f"You will have to buy more than {coupon.condition_rate}. "
                total_amount = "Nan"
        else:
            message = ""
            total_amount = (total_amount - coupon.discount) + delivery_cost
            request.session['code'] = code

    except ObjectDoesNotExist:
        try:
            voucher = Voucher.objects.get(
                user=request.user,
                voucher_code=code,
            )
            discount = voucher.voucher_offer.discount
            # When if the admin or staff doesn't provide the user valid date ......
            if not voucher.user_valid_to == None:
                if now > voucher.user_valid_to:
                    res = True
                else:
                    res = False
            else:
                res = False

            if now > voucher.voucher_offer.offer_valid_to or res:
                message = "This voucher has been expired"
                total_amount = "Nan"

            elif voucher.count > voucher.voucher_offer.limit:
                message = "You have already used maximum of it"
                total_amount = "Nan"

            elif total_amount < voucher.voucher_offer.condition_rate:
                message = f"You will have to buy more than {voucher.voucher_offer.condition_rate}."
                total_amount = "Nan"
            else:
                total_amount = (total_amount -
                                voucher.voucher_offer.discount) + delivery_cost
                message = ""
                request.session['code'] = code

        except ObjectDoesNotExist:
            message = "Code Doesn't Found"
            request.session['code'] = 'invalidCode'
            total_amount = "Nan"
            discount = "Nan"
            if code == "":
                message = "Plz Enter a Code"

    # redirect Action will get the data from this return...
    if redirect == True:
        return {"amount":total_amount, "discount":discount }

    data = {
        "discount": discount,
        "message": message,
        "total_amount": total_amount,
    }
    return JsonResponse(data)

def VoucherView(request):
    try:
        voucher = Voucher.objects.filter(user=request.user)
        return render(request, 'app/voucher.html', {'vouchers': voucher})
    except ObjectDoesNotExist:
        return None

class ManageAccountView(TemplateView):
    template_name = 'app/manageAccount.html'

    def get(self, request, *args, **kwargs):
        profile = CustomerProfile.objects.get(user = request.user)
        context = {
            "profile": profile
        }
        newCustomerAddress = CustomerAddress.objects.filter(user = request.user)
        if len(newCustomerAddress) > 0:
            defaultAddress = CustomerAddress.objects.get(user = request.user, isDefault = True)
            context["defaultAddress"] = defaultAddress

        return render(request, self.template_name, context = context)

class ProfileView(TemplateView):
    template_name = "app/profile.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            try:
                profile = CustomerProfile.objects.get(user=request.user)
                return render(request, self.template_name,
                              {"profile": profile})
            except:
                return render(request, self.template_name)
        else:
            return redirect('login')

class EditProfileView(View):
    template_name = "app/editprofile.html"

    def get(self, request, *args, **kwargs):
        customerprofile = CustomerProfile.objects.get(user=request.user)
        try:
            birthmonth = customerprofile.birthdate.strftime('%B')
            return render(request, self.template_name, {
                "profile": customerprofile,
                "birthmonth": birthmonth
            })
        except:
            return render(request, self.template_name,
                          {"profile": customerprofile})

    def post(self, request):
        customerprofile = CustomerProfile.objects.get(user=request.user)
        context = {
            "profile":customerprofile
        }
        name = request.POST.get('name')
        year = int(request.POST.get('year'))
        month = request.POST.get('month')
        day = int(request.POST.get('day'))
        gender = request.POST.get('gender')

        if name == "" or len(name) < 3:
            context["nameerror"] = "atleast 3 character Needed"
            attempt1 = "failed"
        else:
            attempt1 = "success"
        
        if year == 0:
            context["yearerror"] = "set it"
            attempt2 = "failed"
        else:
            attempt2 = "success"
        
        if month == "":
            context["montherror"] = "set it"
            attempt3 = "failed"
        else:
            attempt3 = "success"
            month = int(month)
        
        if day == 0:
            context["day"] = "set it"
            attempt4 = "failed"
        else: 
            attempt4 = "success"

        if gender == "":
            context['gendererror'] = "select your gender"
            attempt5 = "failed"
        else:
            attempt5 = "success"

        if attempt1 == "success" and attempt2 == "success" and attempt3 == "success" and attempt4 == "success" and attempt5 == "success":
            customerprofile.full_name = name
            customerprofile.birthdate = datetime.date(year, month, day)
            customerprofile.gender = gender
            customerprofile.save()
            return redirect('profileurlname')
        else:
            return render(request, self.template_name, context=context)

class AddressBookView(TemplateView):
    template_name = "app/addressBook.html"
    def get(self, request, *args, **kwargs):
        newCustomerAddress = CustomerAddress.objects.filter(user = request.user)
        return render(request, self.template_name, {"newaddress":newCustomerAddress})

def defaultAddressMaker(request):
    id = request.GET['id']
    newCustomerAddress1 = CustomerAddress.objects.get(user = request.user, isDefault = True)
    newCustomerAddress1.isDefault = False
    newCustomerAddress1.save()
    newCustomerAddress2 = CustomerAddress.objects.get(id = id)
    newCustomerAddress2.isDefault = True
    newCustomerAddress2.save()
    data = {
        "name":"ibrahim"
    }
    return JsonResponse(data)

class AddAddressView(View):
    template_name = "app/addAddress.html"
    division = Divisions.objects.all()
    districts = Districts.objects.all()
    upazilas = Upazilas.objects.all()
    unions = Unions.objects.all()

    def get(self, request, pk = 'none', *args, **kwargs):
        context = {
            'divisions': self.division,
            'districts': self.districts,
            'upazilas': self.upazilas,
            'unions': self.unions,
        }
        try:
            newCustomerAddress  = CustomerAddress.objects.get(id = pk)
            context['newaddress'] = newCustomerAddress
        except :
            pass

        return render(
            request, self.template_name, context = context)

    def post(self, request, *args, **kwargs):
        fullName = request.POST.get("fullName")
        phoneNumber = request.POST.get("phoneNumber")
        divisionId = request.POST.get("divisionId")
        districtId = request.POST.get("districtId")
        upazilaId = request.POST.get("upazilaId")
        unionId = request.POST.get("unionId")
        address = request.POST.get('address')
        pk = request.POST.get('pk')
    
        context = {
                'divisions': self.division,
                'districts': self.districts,
                'upazilas': self.upazilas,
                'unions': self.unions,
                }

        if fullName == "":
            context["nameerror"] = "Write your name"
            attempt1 = "failed"
        else:
            attempt1 = "success"
            context["fullName"] = fullName

        if phoneNumber == "":
            context["phoneerror"] = "Set you phone number"
            attempt2 = "failed"
        else:
            attempt2 = "success"
            context['phoneNumber'] = phoneNumber

        if divisionId == "default" or divisionId == None:
            context["diverror"] = "Select a divition"
            divattempt = "failed"
            attempt3 = "failed"
        else:
            divattempt = "success"
            attempt3 = "success"

        if districtId == "default" or districtId == None:
            context["diserror"] = "Select a district"
            disattempt = "failed"
            attempt4 = "failed"
        else:
            disattempt = "success"
            attempt4 = "success"

        if upazilaId == 'default' or upazilaId == None:
            context["upaerror"] = "Select a upazila"
            upaattempt = "failed"
            attempt5 = "failed"
        else:
            upaattempt = "success"
            attempt5 = "success"

        if unionId == "default" or unionId == None:
            context["unionerror"] = "Select a union"
            uniattempt = "failed"
            attempt6 = "failed"
        else:
            uniattempt = "success"
            attempt6 = "success"

        if address == "":
            context["addrerror"] = "Give your address"
            attempt7 = "failed"
        else:
            attempt7 = "success"
            context['address'] = address
        
        if not divattempt == "failed":  
            division = Divisions.objects.get(id=divisionId)
            context['divisionName'] = division
            context['divisionId'] = divisionId
        if not disattempt == "failed":
            district = Districts.objects.get(id=districtId)
            context['districtName'] = district
            context['districtId'] = districtId
        if not upaattempt == "failed":
            upazila = Upazilas.objects.get(id=upazilaId)
            context['upazilaName'] = upazila
            context['upazilaId'] = upazilaId
        if not uniattempt == "failed":
            union = Unions.objects.get(id=unionId)
            context['unionName'] = union
            context['unionId'] = unionId

        if pk != None:
            newaddress = CustomerAddress.objects.get(id = pk)
            context["newaddress"] = newaddress

        if attempt1 == "success" and attempt2 == "success" and attempt3 == "success" and attempt4 == "success" and attempt5 == "success" and attempt6 == "success" and attempt7 == "success":
            
            if pk != None:
                newaddress.full_name = fullName
                newaddress.phone_number = phoneNumber
                newaddress.divisions = division
                newaddress.districts = district
                newaddress.upazilas = upazila
                newaddress.unions = union
                newaddress.address = address
                newaddress.save()
                return redirect("/abookurl")
                
            else:                    
                newCustomerAddress = CustomerAddress.objects.filter(user = request.user)
                if len(newCustomerAddress) == 0:
                    CustomerAddress(user = request.user, full_name = fullName, phone_number = phoneNumber, divisions = division, districts = district, upazilas = upazila, unions = union, address = address, isDefault = True).save()
                else:
                    CustomerAddress(user = request.user, full_name = fullName, phone_number = phoneNumber, divisions = division, districts = district, upazilas = upazila, unions = union, address = address).save()
               
                return redirect("/abookurl")
        else:
            return render(request, self.template_name, context = context)

class OrderView(TemplateView):
    template_name = "app/order.html"
    def get(self, request, *args, **kwargs):
        newOrder = Order.objects.filter(user = request.user)
        context = {"orders": newOrder}
        return render(request, self.template_name, context=context)

class CancellationView(TemplateView):
    template_name = "app/cancellation.html"

def Checkout(request):
    newCart = Cart.objects.filter(user = request.user)
    length = len(newCart)
    deliveryCharge = 70
    subTotal = 0
    for cart in newCart:
        subTotal += cart.products_total_cost
    total = subTotal + deliveryCharge
  
    newProfile = CustomerProfile.objects.get(user = request.user)
    newAddress = CustomerAddress.objects.filter(user = request.user)

    if  len(newAddress) < 1:
        return redirect('/abookurl')

    try:
        defaultAddress = CustomerAddress.objects.get(user = request.user, isDefault = True)
    except:
        return redirect('/aaddressurl')
    
    context = {
        "carts" : newCart,
        "len" :length,
        "subTotal" : subTotal,
        "deliveryCharge" : deliveryCharge,
        "profile" : newProfile,
        "newaddress" :newAddress,
        "daddress" : defaultAddress,
        "totalAmount": total
    } 
    if not request.session["code"] == 'none':
        # This function will get the total amount and coupon or voucher discount from the previous VoucherChecker function..
        data = VoucherChecker(request, redirect=True)
        if data['amount'] != "Nan" and data['discount'] != "Nan":
            context["totalAmount"] = data['amount']
            context["discount"] = data['discount']
    else:
        context["totalAmount"] = total 

    return render(request,'app/checkout.html', context = context)

# This function will work when user will click the Edit option on checkout page for changing the shipping address when checking out
def SelectAddressView(request):
    id = request.GET['adrId']
    newCustomerAddress1 = CustomerAddress.objects.get(user = request.user, isDefault = True)
    newCustomerAddress1.isDefault = False
    newCustomerAddress1.save()
    newCustomerAddress2 = CustomerAddress.objects.get(id = id)
    newCustomerAddress2.isDefault = True
    newCustomerAddress2.save()
    address = newCustomerAddress2.address
    union = newCustomerAddress2.unions.name
    upazila = newCustomerAddress2.upazilas.name
    district = newCustomerAddress2.districts.name
    division = newCustomerAddress2.divisions.name
    name = newCustomerAddress2.full_name

    data = {
        'name'  : name,
        "address" : address,
        "union" : union,
        "upazila" : upazila,
        "district" : district,
        "division" : division
    }
    return JsonResponse(data)

# This function will take the unit, unitAmount and size data form the backend and save the data to the session to use it in buynow function
def buyNowDataView(request):
    request.session['buyNowUnit'] = "none"
    request.session['buyNowUnitAmount'] = "none"
    request.session['size'] = "none"
    request.session['buyNowProdId'] = "none"
    unit = request.GET['unit']
    unitAmount = request.GET['unitAmount']
    size = request.GET['size']
    productId = request.GET['prodIdV']
    request.session['buyNowProdId'] = productId
    request.session['buyNowUnit'] = unit
    request.session['buyNowUnitAmount'] = unitAmount
    request.session['initialUnitAmount'] = unitAmount
    request.session['size'] = size

    data = {
        'demo' : 'test'
    }
    return JsonResponse(data)

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
    backendUnitGroup = product.unitGroup
 
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

# This function will show the product info in the buynow page....
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
        if newProduct.unitGroup == "SolidWeight" or newProduct.unitGroup == "LiquidWeight":
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

    # plus and minus action in buy now page will work on this section when product having packet unitGroup...    
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

        # plus and minus action in buy now page will work on this section when product having solid and Liquid weight unitGroup...  
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

            if newProduct.unitGroup == "SolidWeight":
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
                                
            if newProduct.unitGroup == "LiquidWeight":
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

def buyNowVoucherCheckerView(request):
    code = request.GET['codeV']
    subTotal = request.session['buyNowSubTotal']
    shoppingCost = 70
    now = timezone.now()
    data = {}
    try:
        coupon = Coupon.objects.get(
            coupon_code = code,
            valid_from__lte = now,
            valid_to__gte= now,
            active = True
        )
        discount = coupon.discount
        if not coupon.condition_rate == None:
            if subTotal >= coupon.condition_rate:
                total = (subTotal - discount)+ shoppingCost
                data['message'] = ""
                data['total'] = total
                data['discount'] = discount
                request.session['buyNowTotal'] = total
                request.session['buyNowDiscount'] = discount
            else:
                message = f"You will have to buy more than {coupon.condition_rate}. "
                data['message'] = message
        else:
            total = (subTotal - discount)+ shoppingCost
            data['total'] = total
            data['message'] = ""
            data['discount'] = discount
            request.session['buyNowTotal'] = total
            request.session['buyNowDiscount'] = discount

    except ObjectDoesNotExist:
        try:
            voucher = Voucher.objects.get(
                user = request.user,
                voucher_code = code,
            )
            discount = voucher.voucher_offer.discount
            if not voucher.user_valid_to == None:
                if now > voucher.user_valid_to:
                    result = True
                else:
                    result = False
            else:
                result = False            
            if now > voucher.voucher_offer.offer_valid_to or result:
                data['message'] = "This voucher has been expired"
            elif voucher.count > voucher.voucher_offer.limit:
                data['message'] = "you have already used maximum of it"
            elif subTotal < voucher.voucher_offer.condition_rate:
                message = f"You will have to buy more than {voucher.voucher_offer.condition_rate}."
                data['message'] = message
            else:
                total = (subTotal - discount) + shoppingCost
                data['message'] = ""
                data['total'] = total
                data['discount'] = discount
                request.session['buyNowTotal'] = total
                request.session['buyNowDiscount'] = discount
        except:
            data['message'] = "Code Doesn't Found"
            if code == "":
                data['message'] = "Plz Enter a Code"

    return JsonResponse(data)

class paymentPageView(TemplateView):
    template_name = "app/paymentPage.html"
    
    # this Section will work for carted Products
    def get (self, request, buyNowTunnel = False,  *args, **kwargs):
        if buyNowTunnel == False:
            newCart = Cart.objects.filter(user = request.user)
            length = len(newCart)
            shippingCost = 70
            subTotal = 0
            for cart in newCart:
                subTotal += cart.products_total_cost
            total = subTotal + shippingCost
        
            newProfile = CustomerProfile.objects.get(user = request.user)
            newAddress = CustomerAddress.objects.filter(user = request.user)

            if  len(newAddress) < 1:
                return redirect('/abookurl')

            try:
                defaultAddress = CustomerAddress.objects.get(user = request.user, isDefault = True)
            except:
                return redirect('/aaddressurl')
            
            context = {
                "carts" : newCart,
                "len" :length,
                "subTotal" : subTotal,
                "shippingCost" : shippingCost,
                "profile" : newProfile,
                "newaddress" :newAddress,
                "daddress" : defaultAddress,
                "from": "cart"
            } 
            if not request.session["code"] == 'none':
                # This function will get the total amount and coupon or voucher discount from the previous VoucherChecker function..
                data = VoucherChecker(request, redirect=True)
                if data['amount'] != "Nan" and data['discount'] != "Nan":
                    context["totalAmount"] = data['amount']
                    context["discount"] = data['discount']
            else:
                context["totalAmount"] = total 
        
        # This section will work for buyed now Products.......
        if not buyNowTunnel == False:
            context = {}
            newProfile = CustomerProfile.objects.get(user = request.user)
            newAddress = CustomerAddress.objects.filter(user = request.user)
            shippingCost = 70
            if  len(newAddress) < 1:
                return redirect('/abookurl')
            try:
                defaultAddress = CustomerAddress.objects.get(user = request.user, isDefault = True)
            except:
                return redirect('/aaddressurl')
            context['profile'] = newProfile
            context['newaddress'] = newAddress
            context['daddress'] = defaultAddress
            context['subTotal'] = request.session['buyNowSubTotal']
            context['shippingCost'] = shippingCost
            context['totalAmount'] = request.session['buyNowTotal']
            context['buyNowDiscount'] = request.session['buyNowDiscount']
            context['from'] = "buyNow"

        return render(request,self.template_name, context = context)
            
def buyNowOrderMakerView(request):
    user = request.user
    productId = request.session['buyNowProdId']
    product = Product.objects.get(id = productId)
    profile = CustomerProfile.objects.get(user = user)
    defaultAddress = CustomerAddress.objects.get(user = user, isDefault = True)
    unit = request.session['buyNowUnit']
    unitAm = request.session['buyNowUnitAmount']
    if unitAm == 'none':
        unitAmount = 0
    else:
        unitAmount = float(unitAm)
    size = request.session['size']
    quan = request.session['buyNowQuantity']
    if quan == "none":
        quantity = 0
    else:
        quantity = int(quan)
    subTotal = float(request.session['buyNowSubTotal'])
    total =  float(request.session['buyNowTotal'])
    
    Order(user = user, profile = profile, address = defaultAddress, product = product, quantity = quantity, unit = unit, unitAmount = unitAmount, size = size, subTotal = subTotal, Total = total).save()
    if product.unitGroup == "Packet" or product.unitGroup == "ShoeSize" or product.unitGroup == "ClothSize":
        product.ProductStock -= quantity
        product.save()

    del request.session["buyNowProdId"]
    del request.session["buyNowUnit"]
    del request.session["buyNowUnitAmount"]
    del request.session["size"]
    del request.session["buyNowQuantity"]
    del request.session["buyNowSubTotal"]
    del request.session["buyNowTotal"]
    return redirect('/orderurl')

def cartOrderMakerView(request):
    user = request.user
    newCart = Cart.objects.filter(user = user) 
    profile = CustomerProfile.objects.get(user = user)
    defaultAddress = CustomerAddress.objects.get(user = user, isDefault = True)
    shippingCost = 70
    subTotal = 0
    for cart in newCart:
        subTotal += cart.products_total_cost
    total = subTotal + shippingCost
    if not request.session["code"] == 'none':
        # This function will get the total amount and coupon or voucher discount from the previous VoucherChecker function..
        data = VoucherChecker(request, redirect=True)
        if data['amount'] != "Nan" and data['discount'] != "Nan":
            newtotal = data['amount']
            discount = data['discount']
        else:
            newtotal = total
    else:
        newtotal = total
        discount = 0
    
    for cart in newCart:
        Order(user = user, profile = profile, address = defaultAddress, product = cart.product, quantity = cart.quantity, unit = cart.unit, unitAmount = cart.unit_amount, size = cart.size, subTotal = subTotal, Total = newtotal).save()
        cart.delete()
        if cart.product.unitGroup == "Packet" or cart.product.unitGroup == "ShoeSize" or cart.product.unitGroup == "ClothSize":
            cart.product.ProductStock -= cart.quantity
            cart.product.save()
    del request.session["code"]
    return redirect('/orderurl')



