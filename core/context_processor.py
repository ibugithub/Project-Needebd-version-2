from django.conf import settings
from .models import Cart, CustomerProfile, Footer_Colum1, Footer_Colum2, Footer_Colum3, Footer_Colum4
def cart_item(request):
    item = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user)
        item = len(cart)
    return {
        'item' :item
    }

def profilepic(request):
    try:
        profile = CustomerProfile.objects.get(user = request.user)
        if profile.image:
            profilepic = profile.image.url
        else :
            profilepic = '/static/app/image/user.svg'           
        return {
            "image" : profilepic
        }
    except:
        return {
            "image": '/static/app/image/user.svg'
        }

def footerCol1(request):
    footer1 = Footer_Colum1.objects.all()
    return {
        'footer1' : footer1
    }

def footerCol2(request):
    footer2 = Footer_Colum2.objects.all()
    return {
        'footer2' : footer2
    }

def footerCol3(request):
    footer3 = Footer_Colum3.objects.all()
    return {
        'footer3' : footer3
    }

def footerCol4(request):
    footer4 = Footer_Colum4.objects.all()
    return {
        'footer4' : footer4
    }