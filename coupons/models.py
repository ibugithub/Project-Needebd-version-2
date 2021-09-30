from django.core import validators
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
import random
# Create your models here.

User = get_user_model()

class Coupon(models.Model):
    coupon_code       = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to   = models.DateTimeField()
    condition_rate = models.PositiveIntegerField(blank=True, null=True)
    discount   = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active     = models.BooleanField(default=False)

    def __str__(self):
        return self.coupon_code



class Voucher(models.Model): 
    title = models.CharField(max_length=30, null= True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    voucher_code = models.CharField(max_length=25, blank = True)
    valid_from   = models.DateTimeField()
    valid_to     = models.DateTimeField()
    condition_rate = models.PositiveIntegerField()
    discount      = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(500)])
    count         = models.PositiveIntegerField(validators=[MinValueValidator(1)],default=1)
    limit         = models.PositiveIntegerField(validators=[MinValueValidator(1)], default = 1)

    def __str__(self):
        return str(self.voucher_code)
    
    def save(self, *args, **kwargs):
        patt = ['a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I', 'j','J','K','k','l','L','m','M','n','o', 'N','O','p','P','q','Q','r','s','S', 't', 'T','u','U','v','V','w','W','x','X','y','Y','z','Z',1,2,3,4,5,6,7,8,9]
        number_list = [x for x in patt]
        code_items = []

        for i in range(25):
            num = random.choice(number_list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        self.voucher_code = code_string
        super().save(*args, **kwargs)


class VoucherOffer(models.Model):
    title     = models.CharField(max_length=40)
    offer_valid_from = models.DateTimeField()
    offer_valid_to   = models.DateTimeField()
    user_valid_from  = models.DateTimeField()
    user_valid_to     = models.DateTimeField()
    discount   = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(500)])
    condition_rate = models.PositiveIntegerField()
    limit = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=False)