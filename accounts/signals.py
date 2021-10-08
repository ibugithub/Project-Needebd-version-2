from .models import User, Code
from django.db.models.signals import post_save
from django.dispatch import receiver
from coupons.models import Voucher, VoucherOffer
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_save, sender= User)
def post_save_generate_code(sender, instance, created, *args, **kwargs):
    if created:
        Code.objects.create(user=instance)
        try:
            registrationoffer = VoucherOffer.objects.get(title = 'RegistrationOffer', active = True)
            if instance.timestamp > registrationoffer.offer_valid_from and instance.timestamp < registrationoffer.offer_valid_to:
                Voucher.objects.create(
                    voucher_offer = registrationoffer,
                    user = instance, 
                    )  
        except: ObjectDoesNotExist
      