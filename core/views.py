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
                     Districts, Unions, Upazilas, CustomerAddress)
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, TemplateView, View
from django.http import JsonResponse
from coupons.models import Coupon, Voucher
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


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
    context_object_name = 'products'
    template_name = 'app/ProductPage.html'

    def get_queryset(self):
        qs = super(ProductPageView, self).get_queryset()
        return qs.filter(product_category__title=self.kwargs.get('category'))

class SingleProductView(Mycontext, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'app/singleproduct.html'

def AddToCartView(request):
    product_id = request.GET['productid']
    unit = request.GET['unit']
    unit_amount = request.GET['unit_amount']
    size = request.GET['Size']
    if request.user.is_authenticated:
        user = request.user
        myproduct = Product.objects.get(id=product_id)

        # Carting the product info for the prduct having KG unit or Liter Unit
        if myproduct.unit == "Kg" or myproduct.unit == "Liter" or myproduct.unit == "ClothPicesSize":
            try:
                cart = Cart.objects.get(user=user,
                                        product=myproduct,
                                        unit=unit,
                                        unit_amount=unit_amount)
                cart.quantity += 1
                cart.save()
            except:
                Cart(user=user,
                     product=myproduct,
                     unit=unit,
                     unit_amount=unit_amount).save()
        elif myproduct.unit == "ClothSize" or myproduct.unit == "ShoeSize":
            try:
                cart = Cart.objects.get(user=user,
                                        product=myproduct,
                                        size=size)
                cart.quantity += 1
                cart.save()
            except:
                Cart(user=user, product=myproduct, size=size).save()
        elif myproduct.unit == "Packet":
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
    if request.user.is_authenticated:
        user = request.user
        product_key = request.GET['id']
        product = Product.objects.get(id=product_key)
        unit = request.GET['unit']
        unit_amount = request.GET['unit_amount']
        size = request.GET['size']

        if product.unit == "Kg" or product.unit == "Liter" or product.unit == "ClothPicesSize":
            cart = Cart.objects.get(user=user,
                                    product=product,
                                    unit=unit,
                                    unit_amount=unit_amount)
            cart.quantity += 1
            cart.save()
        elif product.unit == "ClothSize" or product.unit == "ShoeSize":
            cart = Cart.objects.get(user=user, product=product, size=size)
            cart.quantity += 1
            cart.save()
        elif product.unit == "Packet":
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

        if product.unit == "Liter" or product.unit == "Kg" or product.unit == "ClothPicesSize":
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
        elif product.unit == "ClothSize" or product.unit == "ShoeSize":
            cart = Cart.objects.get(user=user, product=product, size=size)
            if cart.quantity >= 1:
                cart.quantity -= 1
                cart.save()
            if cart.quantity <= 0:
                cart.delete()
                Item = itemcount()
        elif product.unit == "Packet":
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
    user = request.user
    product_key = request.GET['prod_id']
    product = Product.objects.get(id=product_key)
    unit = request.GET['unit']
    unit_amount = request.GET['unit_amount']
    size = request.GET['size']
    if product.unit == "Liter" or product.unit == "Kg" or product.unit == "ClothPicesSize":
        cart = Cart.objects.get(user=user,
                                product=product,
                                unit=unit,
                                unit_amount=unit_amount)
        cart.delete()

    elif product.unit == "ClothSize" or product.unit == "ShoeSize":
        cart = Cart.objects.get(user=user, product=product, size=size)
        cart.delete()

    elif product.unit == "Packet":
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

def VoucherChecker(request):
    carts = Cart.objects.filter(user=request.user)
    total_amount = 0
    for cart in carts:
        total_amount += cart.products_total_cost
    delivery_cost = 70
    code = request.GET['code']
    now = timezone.now()
    try:
        coupon = Coupon.objects.get(coupon_code=code,
                                    valid_from__lte=now,
                                    valid_to__gte=now,
                                    active=True)
        discount = coupon.discount
        if total_amount >= coupon.condition_rate:
            message = ""
            total_amount = (total_amount - coupon.discount) + delivery_cost
        else:
            message = f"You will have to buy more than {coupon.condition_rate}. "
            total_amount = "Nan"
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

        except ObjectDoesNotExist:
            message = "Code Doesn't Found"
            total_amount = "Nan"
            discount = "Nan"
            if code == "":
                message = "Plz Enter a Code"
    data = {
        "discount": discount,
        "message": message,
        "total_amount": total_amount,
    }
    return JsonResponse(data)

def VoucherView(request):
    # vcode = request.GET['dcode']
    # print(vcode)
    try:
        voucher = Voucher.objects.filter(user=request.user)
        return render(request, 'app/voucher.html', {'vouchers': voucher})
    except ObjectDoesNotExist:
        return None

class ManageAccountView(TemplateView):
    template_name = 'app/manageAccount.html'

    def get(self, request, *args, **kwargs):
        profile = CustomerProfile.objects.get(user = request.user)
        return render(request, self.template_name, {"profile": profile})

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
            print("name is not here")
        else:
            attempt1 = "success"
            print('name is here')
        
        print("name is", name)
        print(name == "")
        print(type(name))
        
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

        print(attempt1)
        print(attempt2)
        print(attempt3)
        print(attempt4)
        print(attempt5)
        print(month)
        print("...", gender)
        if attempt1 == "success" and attempt2 == "success" and attempt3 == "success" and attempt4 == "success" and attempt5 == "success":
            print("condition matched")
            customerprofile.full_name = name
            customerprofile.birthdate = datetime.date(year, month, day)
            print("....",gender)
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

class AddAddressView(View):
    template_name = "app/addAddress.html"
    division = Divisions.objects.all()
    districts = Districts.objects.all()
    upazilas = Upazilas.objects.all()
    unions = Unions.objects.all()

    def get(self, request, pk = 'none', *args, **kwargs):
        print("...",pk)
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
                print("pk is not in here")
                print("The pk is ", pk)
                CustomerAddress(user = request.user, full_name = fullName, phone_number = phoneNumber, divisions = division, districts = district, upazilas = upazila, unions = union, address = address).save()
                return redirect("/abookurl")
        else:
            print("No you can't save all the data")       
            return render(request, self.template_name, context = context)

class OrderView(TemplateView):
    template_name = "app/order.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class CancellationView(TemplateView):
    template_name = "app/cancellation.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
