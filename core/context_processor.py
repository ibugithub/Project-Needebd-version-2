from django.conf import settings
from .models import Cart, CustomerProfile
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
