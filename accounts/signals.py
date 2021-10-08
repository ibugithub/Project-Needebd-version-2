from .models import User, Code
from django.db.models.signals import post_save
from django.dispatch import receiver
from coupons.models import Voucher, VoucherOffer
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta

@receiver(post_save, sender= User)
def post_save_generate_code(sender, instance, created, *args, **kwargs):
    if created:
        Code.objects.create(user=instance)
        try:
            registrationoffer = VoucherOffer.objects.get(title = 'RegistrationOffer', active = True)
            if instance.timestamp > registrationoffer.offer_valid_from and instance.timestamp < registrationoffer.offer_valid_to:
                print("here could be the start of problem")
                valid_to = instance.timestamp + timedelta(days = 20)
                print("problem has been")
                Voucher.objects.create(
                    voucher_offer = registrationoffer,
                    user = instance, 
                    user_valid_to = valid_to
                    )  
        except: ObjectDoesNotExist
      