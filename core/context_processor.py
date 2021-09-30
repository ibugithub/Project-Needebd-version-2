from django.conf import settings
from .models import Cart
def cart_item(request):
    item = 0
    if request.user.is_authenticated:

        cart = Cart.objects.filter(user = request.user)
        item = len(cart)
    return {
        'item' :item
    }
