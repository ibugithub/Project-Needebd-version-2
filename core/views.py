from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.detail import DetailView
from .models import Brand_Logo_row1,Brand_Logo_row2, Brand_Logo_row3, Category, Slider, Mobile_Category,  Footer_Colum1, Footer_Colum2, Footer_Colum3, Footer_Colum4, Product,CategoryWraper, Cart
from django.views import View
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, TemplateView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import json


def test(request):
    unit_value = request.GET['myvalue']
    product_id = request.GET['prod_id']
    print(product_id)
    product = Product.objects.get(id = product_id)
    Cart(user = request.user, product = product, size = unit_value).save()
    
    print(unit_value)
    data = {
        "item" : 'success'
    }
    return JsonResponse(data)


# Create your views here.
class Mycontext(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['footer_colum_1'] = Footer_Colum1.objects.all()
        context['footer_colum_2'] = Footer_Colum2.objects.all()
        context['footer_colum_3'] = Footer_Colum3.objects.all()
        context['footer_colum_4'] = Footer_Colum4.objects.all()
        if self.request.user.is_authenticated:
            carts = Cart.objects.filter(user = self.request.user)
            context['item'] = len(carts)
        return context


class IndexView(Mycontext, ListView):
    model = Category
    template_name = 'app/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uppercategories'] = CategoryWraper.objects.filter(display_wraper__name = 'Upper_Category')
        context['bookandstudy'] = Category.objects.filter(category_wraper__name = 'Books & Study')
        context['cookingessential'] = Category.objects.filter(category_wraper__name = 'Cooking Essential')
        context['electronic'] = Category.objects.filter(category_wraper__name = 'Electronic')
        context['girlsandkids'] = Category.objects.filter(category_wraper__name = 'Girls & Kids')
        context['homeessential'] = Category.objects.filter(category_wraper__name = 'Home Essential')
        context['msliders'] = Slider.objects.filter(device = 'Mobile')
        context['fashion'] = Category.objects.filter(category_wraper__name = 'Fashion')
        context['handmade'] = Category.objects.filter(category_wraper__name = 'Handmade' )
        context['other'] =  Category.objects.filter(category_wraper__name = 'Other')
        context['dsliders'] = Slider.objects.filter(device = 'Desktop')
        context['brand_logo_row1'] = Brand_Logo_row1.objects.all()
        context['brand_logo_row2'] = Brand_Logo_row2.objects.all()
        context['brand_logo_row3'] = Brand_Logo_row3.objects.all()
        context['mobile_category'] = Mobile_Category.objects.all()
        context['shop_with_deals'] = Product.objects.filter(display_wraper__name = 'Shop With Deal')
        context['beauty_products'] = Product.objects.filter(display_wraper__name = 'Beauty Product')
        context['mans_fashions'] = Product.objects.filter(display_wraper__name = 'Mans Fashion')
      
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


class ProductPageView(Mycontext,ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'app/ProductPage.html'
    def get_queryset(self):
        qs = super(ProductPageView, self).get_queryset()
        return qs.filter(product_category__title = self.kwargs.get('category'))
   

class SingleProductView(Mycontext,DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'app/singleproduct.html'

def AddToCartView(request):
    print("it's all right")
    product_id = request.GET['productid']
    unit = request.GET['unit']
    unit_amount = request.GET['unit_amount']
    size = request.GET['Size']
    print("This is the unit", unit)
    print("This is the unit amount", unit_amount)
    print("This is the Size", size)
    if request.user.is_authenticated:
        user = request.user
        myproduct = Product.objects.get(id = product_id)
        print("The product unit is ", myproduct.unit)

        # Carting the product info for the prduct having KG unit or Liter Unit
        if myproduct.unit == "Kg" or myproduct.unit == "Liter" or myproduct.unit  == "ClothPicesSize":
            print("this is 1st function")
            try:
                cart = Cart.objects.get(user = user, product = myproduct, unit =unit, unit_amount = unit_amount)
                cart.quantity +=1
                cart.save()
            except:
                Cart(user = user, product = myproduct, unit = unit, unit_amount = unit_amount).save()
        
        elif myproduct.unit == "ClothSize" or myproduct.unit == "ShoeSize":
            print("this is the 2nd function")
            try:
                cart =Cart.objects.get(user =user, product = myproduct, size = size)
                cart.quantity +=1
                cart.save()
            except:
                Cart(user = user, product = myproduct, size = size).save()

        elif myproduct.unit == "Packet":
            try:
                cart = Cart.objects.get(user = user, product = myproduct)
                cart.quantity +=1
                cart.save()
            except:
                Cart(user = user, product = myproduct).save()

        # try:  
        #     cart = Cart.objects.get(user= user, product = myproduct, size = size)
        #     cart.quantity += 1
        #     cart.save()
        #     print(cart.quantity)
        # except:
        #     Cart(user = user, product = myproduct, size = size).save()
    
    data = {
        'name': "ibrahim"
    }
    return JsonResponse(data)


class ShowCartView(Mycontext, TemplateView):
    template_name = 'app/Cartpage.html'

    def get(self, request, *args, **kwargs):
        print("now i'm in showcart")
        if request.user.is_authenticated:
            user = request.user
            carts = Cart.objects.filter(user = user)

            # Total_products_cost = 0
            # for cart in carts:
            #     Total_products_cost += cart.products_cost
            # print(sum)
            # delivery_charge = 70
            # Total_Cost = Total_products_cost + delivery_charge

            return render(request, self.template_name ,{'carts':carts})
        else:
            return redirect('/accounts/login/')


def PlusCartView(request):
    if request.user.is_authenticated:
        product_key = request.GET['id']
        psize = request.GET['size']
        product = Product.objects.get(id = product_key)
        try:
            cart = Cart.objects.get(user = request.user, product = product, size =psize)
        except:
            cart = Cart.objects.get(user = request.user, product = product)
        cart.quantity += 1
        cart.save()
    


        data = {
            'quantity' : cart.quantity,
            'total_products_cost': cart.products_cost
        }
        
        return JsonResponse(data)


def MinusCartView(request):
    if request.user.is_authenticated:
        product_key = request.GET['id']
        product = Product.objects.get(id = product_key)
        cart = Cart.objects.get(user= request.user, product = product)       
        if cart.quantity >= 1:
            cart.quantity -= 1
            cart.save()       
        if cart.quantity == 0:
            cart.delete()
            
        newcart = Cart.objects.filter(user = request.user)
        cartCount = len(newcart)
        if cartCount <= 0:
            cartCount = 0

        data = {
            'quantity' : cart.quantity,
            'total_products_cost': cart.products_cost,
            'cartCount': cartCount

        }
        return JsonResponse(data)


def RemoveCartView(request):
    product_key = request.GET['prod_id']
    product = Product.objects.get(id = product_key)
    cart = Cart.objects.get(user = request.user, product = product)
    cart.delete()
    cart = Cart.objects.filter(user = request.user)
    cartCount = len(cart)
    if cartCount <= 0:
        cartCount = 0
    data = {
        'cartCount' : cartCount,
    }
    return JsonResponse(data)



    