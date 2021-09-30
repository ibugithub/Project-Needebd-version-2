from django.contrib import admin
from .models import Coupon, Voucher, VoucherOffer
# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code', 'valid_from', 'valid_to','condition_rate', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['coupon_code']

admin.site.register(Coupon, CouponAdmin)

class VoucherAdmin(admin.ModelAdmin):
    list_display = ['user','title', 'voucher_code', 'valid_from', 'valid_to', 'condition_rate', 'discount', 'count', 'limit']

class VoucherOfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'offer_valid_from', 'offer_valid_to','user_valid_from','user_valid_to','condition_rate', 'discount', 'limit', 'active']

admin.site.register(Voucher,VoucherAdmin)
admin.site.register(VoucherOffer, VoucherOfferAdmin)