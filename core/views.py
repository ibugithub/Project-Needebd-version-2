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
    product_id = request.GET['productid']
    unit = request.GET['unit']
    unit_amount = request.GET['unit_amount']
    size = request.GET['Size']
    if request.user.is_authenticated:
        user = request.user
        myproduct = Product.objects.get(id = product_id)

        # Carting the product info for the prduct having KG unit or Liter Unit
        if myproduct.unit == "Kg" or myproduct.unit == "Liter" or myproduct.unit  == "ClothPicesSize":
            try:
                cart = Cart.objects.get(user = user, product = myproduct, unit =unit, unit_amount = unit_amount)
                cart.quantity +=1
                cart.save()
            except:
                Cart(user = user, product = myproduct, unit = unit, unit_amount = unit_amount).save()       
        elif myproduct.unit == "ClothSize" or myproduct.unit == "ShoeSize":
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
    data = {
        'name': "ibrahim"
    }
    return JsonResponse(data)

class ShowCartView(Mycontext, TemplateView):
    template_name = 'app/Cartpage.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            carts = Cart.objects.filter(user = user)

            Total_products_cost = 0
            Item  = 0
            for cart in carts:
                Total_products_cost += cart.products_total_cost
                Item += 1
            delivery_cost = 70
            Total_Cost = Total_products_cost + delivery_cost
            
            if Total_Cost == delivery_cost:
                Total_Cost = 0
 

            return render(request, self.template_name ,{'carts':carts, "Total_Cost": Total_Cost, "Item" : Item})
        else:
            return redirect('/accounts/login/')

def PlusCartView(request):
    if request.user.is_authenticated:
        user = request.user
        product_key = request.GET['id']
        product = Product.objects.get(id = product_key)
        unit = request.GET['unit']
        unit_amount = request.GET['unit_amount']
        size = request.GET['size']
        
        if product.unit == "Kg" or product.unit == "Liter" or product.unit  == "ClothPicesSize":
            cart = Cart.objects.get(user = user, product = product, unit = unit, unit_amount = unit_amount)
            cart.quantity += 1
            cart.save()
        elif product.unit == "ClothSize" or product.unit == "ShoeSize":
            cart =Cart.objects.get(user = user, product = product, size = size)
            cart.quantity += 1
            cart.save()        
        elif product.unit == "Packet":
            cart = Cart.objects.get(user = user, product =product)
            cart.quantity += 1
            cart.save()

        carts = Cart.objects.filter(user = user)
        Total_products_cost = 0
        for tccart in carts:
            Total_products_cost += tccart.products_total_cost
        delivery_charge = 70
        Total_Cost = Total_products_cost + delivery_charge        


        data = {
            'quantity' : cart.quantity,
            'products_total_cost': cart.products_total_cost,
            'Total_Cost' : Total_Cost
        }
        
        return JsonResponse(data)

def MinusCartView(request):
    user = request.user
    if user.is_authenticated:
        product_key = request.GET['id']
        product = Product.objects.get(id = product_key)
        unit = request.GET['unit']
        unit_amount = request.GET['unit_amount']
        size = request.GET['size']
        
        def itemcount():
            Item = 0
            icarts = Cart.objects.filter(user = user)     
            for  icart in icarts:
                Item += 1
            return Item

        if product.unit  == "Liter" or product.unit == "Kg" or product.unit == "ClothPicesSize":
            print("now i'm at the 1st function")
            cart = Cart.objects.get(user = user, product = product, unit = unit, unit_amount = unit_amount)
            if cart.quantity >= 1:
                cart.quantity -= 1
                cart.save()
            if cart.quantity == 0:
                cart.delete()
                Item = itemcount()
        elif product.unit == "ClothSize" or product.unit == "ShoeSize":
            print("now im at teh 2nd function")
            cart = Cart.objects.get(user = user, product = product, size = size)
            if cart.quantity >= 1:
                cart.quantity -= 1
                cart.save()
            if cart.quantity <= 0:           
                cart.delete()
                Item = itemcount()
        elif product.unit == "Packet":
            print("now i'm at the 3rd function")
            cart = Cart.objects.get(user = user, product =product)
            if cart.quantity >= 1:
                cart.quantity -= 1
                cart.save()
            if cart.quantity <= 0:           
                cart.delete()
                Item = itemcount()
        try:
            Item
        except:
            Item = 'nochange'
        print("This is the Item Count...", Item)  
        newcart = Cart.objects.filter(user = user)
        cartCount = len(newcart)
        if cartCount <= 0:
            cartCount = 0

        carts = Cart.objects.filter(user = user)
        Total_products_cost = 0
        for tccart in carts:
            Total_products_cost += tccart.products_total_cost
        delivery_cost = 70
        Total_Cost = Total_products_cost + delivery_cost 
        if Total_Cost == delivery_cost:
            Total_Cost = 0

        data = {
            'quantity' : cart.quantity,
            'products_total_cost': cart.products_total_cost,
            'cartCount': cartCount,
            "Total_Cost": Total_Cost,
            "Item" : Item
            
        }
        return JsonResponse(data)

def RemoveCartView(request):
    user = request.user
    product_key = request.GET['prod_id']
    product = Product.objects.get(id = product_key)
    unit = request.GET['unit']
    unit_amount = request.GET['unit_amount']
    size = request.GET['size']
    if product.unit  == "Liter" or product.unit == "Kg" or product.unit == "ClothPicesSize":
        cart = Cart.objects.get(user = user, product = product, unit = unit, unit_amount = unit_amount)
        cart.delete()

    elif product.unit == "ClothSize" or product.unit == "ShoeSize":
        cart = Cart.objects.get(user = user, product = product, size = size)
        cart.delete()

    elif product.unit == "Packet":
        cart = Cart.objects.get(user = user, product =product)
        cart.delete()

    cart = Cart.objects.filter(user = request.user)
    cartCount = len(cart)
    if cartCount <= 0:
        cartCount = 0

    carts = Cart.objects.filter(user = user)
    Total_products_cost = 0
    for tccart in carts:
        Total_products_cost += tccart.products_total_cost
    delivery_cost = 70
    Total_Cost = Total_products_cost + delivery_cost 
    if Total_Cost == delivery_cost:
        Total_Cost = 0
    
    data = {
        'cartCount' : cartCount,
        "Total_Cost" : Total_Cost
    }
    return JsonResponse(data)



    