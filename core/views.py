from datetime import date, timedelta
import datetime
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse, resolve_url
from django.views.generic.detail import DetailView
from .models import (Brand_Logo_row1, Brand_Logo_row2, Brand_Logo_row3,
                     Category, CourierServices, Slider, Mobile_Category, Footer_Colum1,
                     Footer_Colum2, Footer_Colum3, Footer_Colum4, Product,
                     CategoryWraper, Cart, CustomerProfile, Divisions,
                     Districts, Unions, Upazilas, CustomerAddress, Order, OrderSummary)
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, TemplateView, View
from django.http import JsonResponse
from coupons.models import Coupon, Voucher
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q


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
    product = Product.objects.get(id=pk)
    category = product.product_category
    relatedProduct = Product.objects.filter(product_category=category)
    paginator = Paginator(relatedProduct, 11)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "product": product,
        "relatedProduct": relatedProduct,
        "showedProductId": pk,
        "page_obj": page_obj
    }
    return render(request, template_name, context=context)

def AddToCartView(request):
    product_id = request.GET['productid']
    unit = request.GET['unit']
    size = request.GET['Size']
    if request.user.is_authenticated:
        user = request.user
        myproduct = Product.objects.get(id=product_id)

        # Carting the product info for the prduct having KG unit or Liter Unit
        if myproduct.ProductGroup == "SolidWeight" or myproduct.ProductGroup == "LiquidWeight" or myproduct.ProductGroup == "ClothPices":
            unit_amount = float(request.GET['unit_amount'])
            try:
                cart = Cart.objects.get(
                    user=user,
                    product=myproduct,
                    unit=unit,
                )
                cart.unit_amount += unit_amount
                cart.save()
            except:
                Cart(user=user,
                     product=myproduct,
                     unit=unit,
                     unit_amount=unit_amount).save()
        elif myproduct.ProductGroup == "Cloth" or myproduct.ProductGroup == "Shoe":
            try:
                cart = Cart.objects.get(user=user,
                                        product=myproduct,
                                        size=size)
                if cart.quantity < cart.product.ProductStock:
                    cart.quantity += 1
                    cart.save()
            except:
                Cart(user=user, product=myproduct, size=size).save()
        elif myproduct.ProductGroup == "Packet":
            try:
                cart = Cart.objects.get(user=user, product=myproduct)
                if cart.quantity < cart.product.ProductStock:
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
        data = {}
        user = request.user
        product_key = request.GET['id']
        product = Product.objects.get(id=product_key)
        unit = request.GET['unit']
        size = request.GET['size']
        unitFrequency = product.unitValue_On_Increase_or_Decrease
        maxUnitValue = product.MaximumUnitValue
        stock = product.ProductStock
        if product.ProductGroup == "SolidWeight" or product.ProductGroup == "LiquidWeight" or product.ProductGroup == "ClothPices":
            cart = Cart.objects.get(
                user=user,
                product=product,
                unit=unit,
            )
            if cart.unit_amount <= stock and cart.unit_amount <= maxUnitValue:
                cart.unit_amount = round(cart.unit_amount + unitFrequency, 2)
                data['warning'] = ""
                if cart.unit_amount >= maxUnitValue:
                    cart.unit_amount = round(maxUnitValue + unitFrequency, 2)
                    data['warning'] = "MaxAmount"
                if cart.unit_amount >= stock:
                    cart.unit_amount = round(stock + unitFrequency, 2)
                    data['warning'] = "StockOut"
            else:
                if cart.unit_amount > stock:
                    data['warning'] = "StockOut"
                if cart.unit_amount > maxUnitValue:
                    data['warning'] = "MaxAmount"
            cart.save()
            data['unitAmount'] = cart.unit_amount

        if product.ProductGroup == "Cloth" or product.ProductGroup == "Shoe" or product.ProductGroup == "Packet":
            if product.ProductGroup == "Cloth" or product.ProductGroup == "Shoe":
                cart = Cart.objects.get(user=user, product=product, size=size)
            elif product.ProductGroup == "Packet":
                cart = Cart.objects.get(user=user, product=product)
            if cart.quantity <= stock:
                cart.quantity += 1
                data['warning'] = ""
                if cart.quantity >= stock:
                    cart.quantity = stock + 1
                    data['warning'] = "StockOut"
            else:
                if cart.quantity > stock:
                    data['warning'] = "StockOut"
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

        data['quantity'] = cart.quantity,
        data["TotalSell_Cost"] = TotalSell_Cost,
        data['products_total_cost'] = cart.products_total_cost,
        data['Total_Cost'] = Total_Cost,
        
        data['Total_discount'] = Total_discount

        return JsonResponse(data)

def MinusCartView(request):
    request.session['code'] = 'none'
    user = request.user
    if user.is_authenticated:
        data = {}
        product_key = request.GET['id']
        product = Product.objects.get(id=product_key)
        unit = request.GET['unit']
        size = request.GET['size']
        unitFrequency = product.unitValue_On_Increase_or_Decrease
        minUnitValue = product.MinimumUnitValue
        stock = product.ProductStock

        def itemcount():
            Item = 0
            icarts = Cart.objects.filter(user=user)
            for icart in icarts:
                Item += 1
            return Item

        if product.ProductGroup == "LiquidWeight" or product.ProductGroup == "SolidWeight" or product.ProductGroup == "ClothPices":
            cart = Cart.objects.get(
                user=user,
                product=product,
                unit=unit,
            )
            if cart.unit_amount  >= minUnitValue:
                cart.unit_amount = round(cart.unit_amount - unitFrequency, 2)
                data['warning'] = ""
                if cart.unit_amount <= minUnitValue:
                    cart.unit_amount = minUnitValue
                    data['warning'] = ""
                if cart.unit_amount > stock:
                    data['warning'] = "Stock Out"
                if cart.unit_amount > cart.unit_amount:
                    data['warning'] = "MaxAmount"                        
            cart.save()
            data['unitAmount'] = round(cart.unit_amount, 2)
           
        if product.ProductGroup == "Cloth" or product.ProductGroup == "Shoe" or product.ProductGroup == "Packet":
            if product.ProductGroup == "Cloth" or product.ProductGroup == "Shoe":
                cart = Cart.objects.get(user=user, product=product, size=size)
            elif product.ProductGroup == "Packet":
                cart = Cart.objects.get(user=user, product=product)
            if cart.quantity >= 1:
                cart.quantity -= 1
                cart.save()
            if cart.quantity > stock:
                data['warning'] = "StockOut"
            else:
                data['warning'] = ""
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

        data['quantity'] = cart.quantity,
        data["TotalSell_Cost"] = TotalSell_Cost,
        data['products_total_cost'] = cart.products_total_cost,
        data['cartCount'] = cartCount,
        data["Total_Cost"] = Total_Cost,
        data["Item"] = Item,
        data["Total_discount"] = Total_discount

        return JsonResponse(data)

def RemoveCartView(request):
    request.session['code'] = 'none'
    user = request.user
    product_key = request.GET['prod_id']
    product = Product.objects.get(id=product_key)
    unit = request.GET['unit']
    size = request.GET['size']
    if product.ProductGroup == "LiquidWeight" or product.ProductGroup == "SolidWeight" or product.ProductGroup == "ClothPice":
        cart = Cart.objects.get(
            user=user,
            product=product,
            unit=unit,
        )
        cart.delete()

    elif product.ProductGroup == "Cloth" or product.ProductGroup == "Shoe":
        cart = Cart.objects.get(user=user, product=product, size=size)
        cart.delete()

    elif product.ProductGroup == "Packet":
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

def VoucherChecker(request, redirect=False):
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
        return {"amount": total_amount, "discount": discount}

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
        profile = CustomerProfile.objects.get(user=request.user)
        context = {"profile": profile}
        newCustomerAddress = CustomerAddress.objects.filter(user=request.user)
        if len(newCustomerAddress) > 0:
            defaultAddress = CustomerAddress.objects.get(user=request.user,
                                                         isDefault=True)
            context["defaultAddress"] = defaultAddress
        newOrder = Order.objects.filter(
            Q(user=request.user, status='Pending')
            | Q(user=request.user, status='Confirmed')
            | Q(user=request.user, status='On the way')
            | Q(user=request.user, status='Delivered'))
        if len(newOrder) > 0:
            context["orders"] = newOrder
        return render(request, self.template_name, context=context)

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
        context = {"profile": customerprofile}
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
        newCustomerAddress = CustomerAddress.objects.filter(user=request.user)
        return render(request, self.template_name,
                      {"newaddress": newCustomerAddress})

def defaultAddressMaker(request):
    id = request.GET['id']
    newCustomerAddress1 = CustomerAddress.objects.get(user=request.user,
                                                      isDefault=True)
    newCustomerAddress1.isDefault = False
    newCustomerAddress1.save()
    newCustomerAddress2 = CustomerAddress.objects.get(id=id)
    newCustomerAddress2.isDefault = True
    newCustomerAddress2.save()
    data = {"name": "ibrahim"}
    return JsonResponse(data)

def get_json_district(request, *args, **kwargs):
    selected_division_id  = kwargs.get('division')
    districts = list(Districts.objects.filter(division_id = selected_division_id).values())
    return JsonResponse({"data": districts})

def get_json_upazila(request, *args, **kwargs):
    selected_district_id  = kwargs.get('district')
    upazilas = list(Upazilas.objects.filter(district_id = selected_district_id).values())
    return JsonResponse({"data": upazilas})

def get_json_union(request, *args, **kwargs):
    selected_upazila_id = kwargs.get('upazila')
    unions = list(Unions.objects.filter(upazilla_id = selected_upazila_id).values())
    return JsonResponse({"data": unions})

class AddAddressView(View):
    template_name = "app/addAddress.html"
    division = Divisions.objects.all()

    def get(self, request, pk='none', *args, **kwargs):
        context = {
            'divisions': self.division
        }
        try:
            newCustomerAddress = CustomerAddress.objects.get(id=pk)
            context['newaddress'] = newCustomerAddress
            context['disable'] = 'false'
        except:
            pass

        return render(request, self.template_name, context=context)

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
            'divisions': self.division
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
            newaddress = CustomerAddress.objects.get(id=pk)
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
                newCustomerAddress = CustomerAddress.objects.filter(
                    user=request.user)
                if len(newCustomerAddress) == 0:
                    CustomerAddress(user=request.user,
                                    full_name=fullName,
                                    phone_number=phoneNumber,
                                    divisions=division,
                                    districts=district,
                                    upazilas=upazila,
                                    unions=union,
                                    address=address,
                                    isDefault=True).save()
                else:
                    CustomerAddress(user=request.user,
                                    full_name=fullName,
                                    phone_number=phoneNumber,
                                    divisions=division,
                                    districts=district,
                                    upazilas=upazila,
                                    unions=union,
                                    address=address).save()

                return redirect("/abookurl")
        else:
            return render(request, self.template_name, context=context)

class OrderView(TemplateView):
    template_name = "app/order.html"

    def get(self, request, *args, **kwargs):
        newOrder = Order.objects.filter(
            Q(user=request.user, status='Pending')
            | Q(user=request.user, status='Confirmed')
            | Q(user=request.user, status='On the way')
            | Q(user=request.user, status='Delivered'))
        context = {"orders": newOrder}
        return render(request, self.template_name, context=context)

def CancelOrderView(request, pk):
    order = Order.objects.get(id=pk)
    order.status = 'Canceled'
    order.save()
    summary = order.ordersummary_set.first()
    cancelOrder = summary.orderItem.get(id = pk)
    CPrdCost = cancelOrder.singleProductCost
    summary.subTotal -= CPrdCost
    summary.total -= CPrdCost
    summary.save()
    productGroup = order.product.ProductGroup
    if productGroup == "Cloth" or productGroup == "Shoe" or productGroup == "Packet":
        order.product.ProductStock += order.quantity
        order.product.save()
    if productGroup == "SolidWeight" or productGroup == "LiquidWeight":
        order.product.ProductStock += order.unitAmount
        order.product.save()



    
    return redirect('/orderurl')

class CancellationView(TemplateView):
    template_name = "app/cancellation.html"

    def get(self, request, *args, **kwargs):
        cancelOrder = Order.objects.filter(user=request.user,
                                           status='Canceled')
        return render(request, self.template_name, {'corder': cancelOrder})

class ReturnedOrderView(TemplateView):
    template_name = "app/returnedOrder.html"

    def get(self, request, *args, **kwargs):
        returnedOrder = Order.objects.filter(user=request.user,
                                             status='Returned')
        return render(request, self.template_name, {'rorder': returnedOrder})

def ReturnOrderView(request, pk):
    order = Order.objects.get(id=pk)
    order.status = 'Returned'
    order.save()
    return redirect('/orderurl')

def Checkout(request):
    newCart = Cart.objects.filter(user=request.user)
    length = len(newCart)
    deliveryCharge = 70
    subTotal = 0
    for cart in newCart:
        subTotal += cart.products_total_cost
    total = subTotal + deliveryCharge

    newProfile = CustomerProfile.objects.get(user=request.user)
    newAddress = CustomerAddress.objects.filter(user=request.user)

    if len(newAddress) < 1:
        return redirect('/abookurl')

    try:
        defaultAddress = CustomerAddress.objects.get(user=request.user,
                                                     isDefault=True)
    except:
        return redirect('/aaddressurl')

    context = {
        "carts": newCart,
        "len": length,
        "subTotal": subTotal,
        "deliveryCharge": deliveryCharge,
        "profile": newProfile,
        "newaddress": newAddress,
        "daddress": defaultAddress,
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

    return render(request, 'app/checkout.html', context=context)

# This function will work when user will click the Edit option on checkout page for changing the shipping address when checking out
def SelectAddressView(request):
    id = request.GET['adrId']
    newCustomerAddress1 = CustomerAddress.objects.get(user=request.user,
                                                      isDefault=True)
    newCustomerAddress1.isDefault = False
    newCustomerAddress1.save()
    newCustomerAddress2 = CustomerAddress.objects.get(id=id)
    newCustomerAddress2.isDefault = True
    newCustomerAddress2.save()
    address = newCustomerAddress2.address
    union = newCustomerAddress2.unions.name
    upazila = newCustomerAddress2.upazilas.name
    district = newCustomerAddress2.districts.name
    division = newCustomerAddress2.divisions.name
    name = newCustomerAddress2.full_name

    data = {
        'name': name,
        "address": address,
        "union": union,
        "upazila": upazila,
        "district": district,
        "division": division
    }
    return JsonResponse(data)

# This function will take the unit, unitAmount and size data form the backend and save the data to the session to use it in buynow function
def buyNowDataView(request):
    request.session['buyNowUnitAmount'] = "none"
    request.session['size'] = "none"
    request.session['buyNowProdId'] = "none"
    unitAmount = request.GET['unitAmount']
    size = request.GET['size']
    productId = request.GET['prodIdV']
    request.session['buyNowProdId'] = productId
    request.session['buyNowUnitAmount'] = unitAmount
    request.session['size'] = size
    data = {'demo': 'test'}
    return JsonResponse(data)

def minMaxUnitCheckerView(request):
    request.session['buyNow_Unit_SellingCost'] = "none"
    request.session['buyNow_Total_SellingCost'] = "none"
    request.session['buyNow_Unit_DiscountedCost'] = "none"
    request.session['buyNow_Total_DiscountedCost'] = "none"
    data = {}
    productId = request.GET['prodIdV']
    fontendUnitAmount = float(request.GET['unitAmountV'])
    product = Product.objects.get(id=productId)
    buyNowSellingCost = product.selling_prize
    buyNowDiscountedCost = product.discounted_prize
    backendUnit = product.unit
    minUnitValue = product.MinimumUnitValue
    maxUnitValue = product.MaximumUnitValue
    backendUnitGroup = product.ProductGroup
    stock = product.ProductStock

    if backendUnitGroup == "SolidWeight" or backendUnitGroup == "LiquidWeight" or backendUnitGroup == "ClothPices":

        if fontendUnitAmount >= minUnitValue and fontendUnitAmount <= maxUnitValue and fontendUnitAmount <= stock:
            data["message"] = ""
            data["attempt"] = True
            request.session['buyNowUnitAmount'] = fontendUnitAmount
            converted_Total_SellingCost = buyNowSellingCost * fontendUnitAmount
            converted_Total_DiscountedCost = buyNowDiscountedCost * fontendUnitAmount
            request.session['buyNow_Unit_SellingCost'] = buyNowSellingCost
            request.session['buyNow_Total_SellingCost'] = round(
                converted_Total_SellingCost, 2)
            request.session[
                'buyNow_Unit_DiscountedCost'] = buyNowDiscountedCost
            request.session['buyNow_Total_DiscountedCost'] = round(
                converted_Total_DiscountedCost, 2)
        else:
            if fontendUnitAmount < minUnitValue:
                message = f"you have to select  atleast {minUnitValue} {backendUnit} for this product"
                data["message"] = message
                data["attempt"] = False
            elif fontendUnitAmount > maxUnitValue:
                message = f"you can't select  more than {maxUnitValue} {backendUnit} for this product"
                data["message"] = message
                data["attempt"] = False
            elif fontendUnitAmount > stock:
                message = f"only {stock} {backendUnit} is available for this product now"
                data["message"] = message
                data["attempt"] = False

    return JsonResponse(data)

# This function will show the product info in the buynow page....
def Buynow(request, pk=None):
    request.session['buyNowSubTotal'] = 'none'
    request.session['buyNowTotal'] = 'none'
    request.session['buyNowDiscount'] = 'none'
    request.session['buyNowQuantity'] = "none"
    context = {}

    try:
        defaultAddress = CustomerAddress.objects.get(user=request.user,
                                                     isDefault=True)
    except:
        return redirect('/aaddressurl')
    newProfile = CustomerProfile.objects.get(user=request.user)
    newAddress = CustomerAddress.objects.filter(user=request.user)
    if len(newAddress) < 1:
        return redirect('/abookurl')
    context['newaddress'] = newAddress
    context["daddress"] = defaultAddress
    context["profile"] = newProfile

    # initial product info will be shown by this section
    if pk != None:
        # This section will work for packet product.............
        request.session['buyNowProdId'] = pk
        newProduct = Product.objects.get(id=pk)
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
            context['buyNowUnitAmount'] = request.session['buyNowUnitAmount']
            context['Unit_SellingCost'] = request.session[
                'buyNow_Unit_SellingCost']
            context['Total_SellingCost'] = request.session[
                'buyNow_Total_SellingCost']
            context['Unit_DiscountedCost'] = request.session[
                'buyNow_Unit_DiscountedCost']
            context["Total_DiscountedCost"] = request.session[
                'buyNow_Total_DiscountedCost']
            subTotal2 = float(request.session['buyNow_Total_DiscountedCost'])
            Total2 = subTotal2 + shippingCost
            context['subtotal'] = subTotal2
            context['total'] = Total2
            request.session['buyNowSubTotal'] = subTotal2
            request.session['buyNowTotal'] = Total2

        return render(request, 'app/buyNowCheckout.html', context=context)

    # plus and minus action in buy now page will work on this section when product having packet ProductGroup...
    if pk == None:
        Group = request.GET['Group']
        if Group == "packet":
            productId = request.GET['productId']
            quantity = int(request.GET['quantity'])
            request.session['buyNowQuantity'] = quantity
            newProduct = Product.objects.get(id=productId)
            shippingCost = 70
            subTotal = newProduct.discounted_prize * quantity
            total = subTotal + shippingCost
            request.session['buyNowSubTotal'] = subTotal
            request.session["buyNowTotal"] = total
            data = {'subTotal': subTotal, "total": total}

        # plus and minus action in buy now page will work on this section when product having solid and Liquid weight ProductGroup...
        elif Group == "nonpacket":
            data = {}
            action = request.GET['action']
            prouductId = request.GET['productId']
            newProduct = Product.objects.get(id=prouductId)
            unitAmount = float(request.session['buyNowUnitAmount'])
            unitFrequency = newProduct.unitValue_On_Increase_or_Decrease
            minUnitValue = newProduct.MinimumUnitValue
            maxUnitValue = newProduct.MaximumUnitValue
            stock = newProduct.ProductStock            

            if newProduct.ProductGroup == "SolidWeight" or newProduct.ProductGroup == "LiquidWeight":                           
                if action == "plus":
                    if unitAmount <= stock and unitAmount <= maxUnitValue:
                        unitAmount += unitFrequency
                        data['warning'] = ""
                        if unitAmount >= maxUnitValue:
                            unitAmount = maxUnitValue + unitFrequency
                            data['warning'] = "MaxAmount"

                        if unitAmount >= stock:
                            unitAmount = stock + unitFrequency
                            data['warning'] = "Stock Out"
                    else:
                        if unitAmount > stock:
                            data['warning'] = "Stock Out"
                        if unitAmount > maxUnitValue:
                            data['warning'] = "MaxAmount"

                if action == "minus":
                    if unitAmount  > minUnitValue:
                        unitAmount -= unitFrequency
                        data['warning'] = ""
                        if unitAmount <= minUnitValue:
                            unitAmount = minUnitValue
                            data['warning'] = ""
                        if unitAmount > stock:
                            data['warning'] = "Stock Out"
                        if unitAmount > maxUnitValue:
                            data['warning'] = "MaxAmount"
                    else:
                        data['warning'] = ""                        
                
                        
            data['unitAmount'] = round(unitAmount, 2)
            request.session['buyNowUnitAmount'] = unitAmount
            sellingCost = round(newProduct.selling_prize * unitAmount, 2)
            discountedCost = round(newProduct.discounted_prize * unitAmount, 2)
            data['sellingCost'] = sellingCost
            data['discountedCost'] = discountedCost
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
        coupon = Coupon.objects.get(coupon_code=code,
                                    valid_from__lte=now,
                                    valid_to__gte=now,
                                    active=True)
        discount = coupon.discount
        if not coupon.condition_rate == None:
            if subTotal >= coupon.condition_rate:
                total = (subTotal - discount) + shoppingCost
                data['message'] = ""
                data['total'] = total
                data['discount'] = discount
                request.session['buyNowTotal'] = total
                request.session['buyNowDiscount'] = discount
            else:
                message = f"You will have to buy more than {coupon.condition_rate}. "
                data['message'] = message
        else:
            total = (subTotal - discount) + shoppingCost
            data['total'] = total
            data['message'] = ""
            data['discount'] = discount
            request.session['buyNowTotal'] = total
            request.session['buyNowDiscount'] = discount

    except ObjectDoesNotExist:
        try:
            voucher = Voucher.objects.get(
                user=request.user,
                voucher_code=code,
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
    def get(self, request, buyNowTunnel=False, *args, **kwargs):
        if buyNowTunnel == False:
            newCart = Cart.objects.filter(user=request.user)
            length = len(newCart)
            shippingCost = 70
            subTotal = 0
            for cart in newCart:
                subTotal += cart.products_total_cost
            total = subTotal + shippingCost

            newProfile = CustomerProfile.objects.get(user=request.user)
            newAddress = CustomerAddress.objects.filter(user=request.user)

            if len(newAddress) < 1:
                return redirect('/abookurl')

            try:
                defaultAddress = CustomerAddress.objects.get(user=request.user,
                                                             isDefault=True)
            except:
                return redirect('/aaddressurl')

            context = {
                "carts": newCart,
                "len": length,
                "subTotal": subTotal,
                "shippingCost": shippingCost,
                "profile": newProfile,
                "newaddress": newAddress,
                "daddress": defaultAddress,
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
            newProfile = CustomerProfile.objects.get(user=request.user)
            newAddress = CustomerAddress.objects.filter(user=request.user)
            shippingCost = 70
            if len(newAddress) < 1:
                return redirect('/abookurl')
            try:
                defaultAddress = CustomerAddress.objects.get(user=request.user,
                                                             isDefault=True)
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
        context['couriers'] = CourierServices.objects.all()
        return render(request, self.template_name, context=context)

def courierSetter(request):
    courier = request.GET['courierV']
    request.session['courier'] = courier
    data = {}
    return JsonResponse(data)

def buyNowOrderMakerView(request):
    user = request.user
    productId = request.session['buyNowProdId']
    product = Product.objects.get(id=productId)
    profile = CustomerProfile.objects.get(user=user)
    defaultAddress = CustomerAddress.objects.get(user=user, isDefault=True)
    unit = product.unit
    unitAmount = request.session['buyNowUnitAmount']
    size = request.session['size']
    quantity = request.session['buyNowQuantity']
    subTotal = float(request.session['buyNowSubTotal'])
    total = float(request.session['buyNowTotal'])
    courierName = request.session['courier']
    courier = CourierServices.objects.get(name = courierName)
    deliveryDate = timezone.now() + timedelta(7)
    shippingCost = 70
    discount = request.session['buyNowDiscount']
    if discount == "none":
        discount = 0

    # This section will save the order for product having cloth and shoe and packet productGroup
    if product.ProductGroup == "Cloth" or product.ProductGroup == "Shoe" or product.ProductGroup == "Packet":
        if quantity > product.ProductStock:
            return redirect('/buynow/'+str(product.id))
        Order(
            user=user,
            profile=profile,
            address=defaultAddress,
            product=product,
            quantity=quantity,
            size=size,
            singleProductCost = subTotal,
            courier = courier,
            delivery_date = deliveryDate,
            shippingCost = shippingCost
            ).save()
        product.ProductStock -= quantity
        product.save()
 
    # This section will save the order for product having solidweight and liquidweight and ClothPicessweight
    if product.ProductGroup == "SolidWeight" or product.ProductGroup == "LiquidWeight" or product.ProductGroup == "ClothPices":
        if unitAmount > product.ProductStock:
            return redirect('/buynow/'+str(product.id))            
        Order(
            user=user,
            profile=profile,
            address=defaultAddress,
            product=product,
            unit=unit,
            unitAmount=unitAmount,
            singleProductCost = total,
            courier = courier,
            delivery_date = deliveryDate,
            shippingCost = shippingCost
            ).save()
        product.ProductStock -= unitAmount
        product.save()
    
        orderSumm = OrderSummary.objects.create()
   
    orderSumm = OrderSummary.objects.create()
    orders = Order.objects.filter(Q(user=request.user, status='Pending', is_summuried = False ))
    for orderItem in orders:
        orderSumm.orderItem.add(orderItem)
        orderItem.is_summuried = True
        orderItem.save()
    orderSumm.subTotal = subTotal
    orderSumm.total = total
    orderSumm.coupon_or_discount = discount
    orderSumm.save()
    request.session["buyNowProdId"] = 'none'
    request.session["buyNowUnit"] = 'none'
    request.session["buyNowUnitAmount"] = 'none'
    request.session["size"] = 'none'
    request.session["buyNowQuantity"] = 'none'
    request.session["buyNowSubTotal"] = 'none'
    request.session["buyNowTotal"] = 'none'
    request.session['courier'] = 'none'
    request.session['buyNowDiscount'] = "none"
    return redirect('/orderurl')

def cartOrderMakerView(request):
    user = request.user
    newCart = Cart.objects.filter(user=user)
    profile = CustomerProfile.objects.get(user=user)
    defaultAddress = CustomerAddress.objects.get(user=user, isDefault=True)
    shippingCost = 70
    subTotal = 0
    courierName = request.session['courier']
    courier = CourierServices.objects.get(name = courierName)
    deliveryDate = timezone.now() + timedelta(7)
    shippingCost = 70
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
        if cart.product.ProductGroup == "Cloth" or cart.product.ProductGroup == "Shoe" or cart.product.ProductGroup == "Packet":
            if cart.quantity > cart.product.ProductStock:
                return redirect("/showcarturl")
            Order(
                user=user,
                profile=profile,
                address=defaultAddress,
                product=cart.product,
                quantity=cart.quantity,
                size=cart.size,
                singleProductCost = cart.products_total_cost,
                courier = courier,
                delivery_date = deliveryDate,
                shippingCost = shippingCost
                ).save()
            cart.delete()
            cart.product.ProductStock -= cart.quantity
            cart.product.save()
            
        if cart.product.ProductGroup == "SolidWeight" or cart.product.ProductGroup == "LiquidWeight" or cart.product.ProductGroup == "ClothPices":
            if cart.unit_amount > cart.product.ProductStock or cart.unit_amount > cart.product.MaximumUnitValue:
                return redirect("/showcarturl")
            Order(
                user=user,
                profile=profile,
                address=defaultAddress,
                product=cart.product, 
                unit=cart.unit,
                unitAmount=cart.unit_amount,
                singleProductCost = cart.products_total_cost,
                courier = courier,
                delivery_date = deliveryDate,
                shippingCost = shippingCost
                ).save()
            cart.delete()
            cart.product.ProductStock -= cart.unit_amount
            cart.product.save()
    orderSumm = OrderSummary.objects.create()
    orders = Order.objects.filter(Q(user=request.user, status='Pending', is_summuried = False ))
    for orderItem in orders:
        orderSumm.orderItem.add(orderItem)
        orderItem.is_summuried = True
        orderItem.save()
    orderSumm.subTotal = subTotal
    orderSumm.total = newtotal
    orderSumm.coupon_or_discount = discount
    orderSumm.save()
    request.session["code"] = 'none'
    return redirect('/orderurl')

def orderToOrderSummery(request, pk):
    order = Order.objects.get(id = pk)
    summary = order.ordersummary_set.first()
    orders = summary.orderItem.filter(Q(user=request.user, status='Pending')
            | Q(user=request.user, status='Confirmed')
            | Q(user=request.user, status='On the way')
            | Q(user=request.user, status='Delivered'))
    context = {
        "orders" : orders,
        "summary": summary
    }
    return render(request, 'app/orderSummary.html', context = context)